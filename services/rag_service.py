from openai import OpenAI
from fastapi import UploadFile
import fitz  # PyMuPDF
import io

class RAGService:
    async def process_rag_query(
        self,
        message: str,
        context_file: UploadFile | None,
        client: OpenAI
    ) -> str:
        try:
            # Si no hay archivo, el contexto está vacío
            if not context_file:
                return "Error: Se requiere un archivo de contexto para esta operación."
            
            context = await self._extract_text_from_file(context_file)

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
            completion = client.chat.completions.create(
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

        except Exception as e:
            print(f"Error: {e}")
            return "Error:"

    async def _extract_text_from_file(self, file: UploadFile) -> str:
        """Helper para extraer texto de archivos PDF o de texto plano."""
        content = await file.read()
        context = ""

        if file.content_type == 'application/pdf':
            # Es un PDF, usamos PyMuPDF para extraer texto
            pdf_document = fitz.open(stream=io.BytesIO(content))
            for page in pdf_document:
                context += page.get_text()
            pdf_document.close()
        else:
            # Asumimos que es un archivo de texto plano
            try:
                context = content.decode('utf-8')
            except UnicodeDecodeError:
                context = content.decode('latin-1')
        
        return context