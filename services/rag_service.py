from openai import OpenAI
from fastapi import UploadFile
import os
import fitz  # PyMuPDF
import io
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTE_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )

    async def process_rag_query(self, message: str, context_file: UploadFile) -> str:
        try:
            context = ""
            content = await context_file.read()

            # --- NUEVO: Procesar el archivo según su tipo (PDF o Texto) ---
            if context_file.content_type == 'application/pdf':
                # Es un PDF, usamos PyMuPDF para extraer texto
                pdf_document = fitz.open(stream=io.BytesIO(content))
                for page in pdf_document:
                    context += page.get_text()
                pdf_document.close()
            else:
                # Asumimos que es un archivo de texto plano
                try:
                    # Intenta decodificar como UTF-8 primero
                    context = content.decode('utf-8')
                except UnicodeDecodeError:
                    # Si falla, intenta con 'latin-1'
                    context = content.decode('latin-1')

            # --- NUEVO: Truncar el contexto para evitar exceder el límite de tokens ---
            # El límite de tokens es ~130k. Usemos un límite de caracteres seguro.
            # 1 token ~ 4 caracteres. 100,000 caracteres ~ 25,000 tokens, lo cual es seguro.
            MAX_CONTEXT_CHARS = 100000
            if len(context) > MAX_CONTEXT_CHARS:
                context = context[:MAX_CONTEXT_CHARS]

            # Create the prompt with the context and user's question for the user role
            user_prompt = f"""Por favor, usa el siguiente contexto para responder la pregunta del usuario.
                            Si la respuesta no se encuentra en el contexto, dilo.

            Contexto:
            {context}

Pregunta del usuario:
            {message}"""

            # Call OpenAI API
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-20b:free",
                messages=[
                    {"role": "system", "content": "Eres un asistente útil y creativo que ayuda a los usuarios a responder preguntas y resolver problemas en español de manera concisa, basándote en el contexto proporcionado."},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # --- NUEVO: Verificación de seguridad para la respuesta ---
            if completion.choices and completion.choices[0].message and completion.choices[0].message.content:
                response = completion.choices[0].message.content
                print(response) # Imprime la respuesta en la consola del servidor
                return response
            return "Error: No se recibió una respuesta válida del modelo."

        except FileNotFoundError:
            return "Error: The specified context file was not found."
        except UnicodeDecodeError:
            return "Error: The context file is not encoded in UTF-8. Please use a UTF-8 encoded file."
        except Exception as e:
            print(f"Error: {e}")
            return "Error:"