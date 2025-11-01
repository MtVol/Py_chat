from schemas.chat_shemas import InputMensage
from openai import OpenAI

def get_chat_response(data_in: InputMensage, client: OpenAI):
    data = data_in.model_dump()
    message = data['message']
    try:
        completion = client.chat.completions.create( # Usa el cliente recibido
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente util y creativo que ayuda a los usuarios a responder preguntas y resolver problemas en español de manera concisa.", 
                },
                {
                    "role": "user",
                    "content": message,
                }
            ])

        # --- NUEVO: Verificación de seguridad para la respuesta ---
        if completion.choices and completion.choices[0].message and completion.choices[0].message.content:
            response = completion.choices[0].message.content
            print(response)
            return response
        return "Error: No se recibió una respuesta válida del modelo."

    except Exception as e:
        print(f"Error: {e}")
        return f"Error:"