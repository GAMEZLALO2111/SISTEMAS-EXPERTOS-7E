import json  # Importa el módulo json para trabajar con archivos JSON
import random  # Importa el módulo random para seleccionar respuestas aleatorias
import re  # Importa el módulo re para trabajar con expresiones regulares

class KnowledgeBase:
    def __init__(self, filename="intents.json"):
        """Inicializa la base de conocimientos con el nombre del archivo."""
        self.filename = filename  # Asigna el nombre del archivo a la variable 'filename'
        self.intents = self.load_knowledge()  # Carga los intents desde el archivo

    def load_knowledge(self):
        """Carga los intents desde el archivo JSON."""
        try:
            # Intenta abrir el archivo y cargar los datos en formato JSON
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)  # Carga los datos del archivo JSON
                return data.get("intents", [])  # Devuelve los intents o una lista vacía si no existen
        except FileNotFoundError:
            # Si el archivo no se encuentra, muestra un mensaje de error y retorna una lista vacía
            print(f"Archivo {self.filename} no encontrado. Se cargará una lista vacía.")
            return []  # Retorna una lista vacía si no se encuentra el archivo
        except json.JSONDecodeError:
            # Si ocurre un error al decodificar el JSON (por ejemplo, si el archivo no es válido), muestra un mensaje de error
            print(f"Error al decodificar el archivo {self.filename}. Asegúrate de que esté en formato JSON.")
            return []  # Retorna una lista vacía si hay un error de decodificación

    def save_knowledge(self):
        """Guarda los intents en el archivo JSON."""
        try:
            # Intenta abrir el archivo en modo escritura y guardar los datos de los intents en formato JSON
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump({"intents": self.intents}, file, indent=4, ensure_ascii=False)  # Escribe los datos en el archivo JSON
        except OSError as e:
            # Si ocurre un error al intentar abrir o escribir el archivo, muestra un mensaje de error
            print(f"Error al guardar el archivo: {e}")  # Muestra el error específico

    def get_answer(self, question):
        """Devuelve una respuesta para la pregunta dada, si existe."""
        for intent in self.intents:  # Recorre todos los intents cargados
            # Si encuentra un patrón en los intents que coincida con la pregunta (usando expresiones regulares)
            if any(re.search(pattern, question, re.IGNORECASE) for pattern in intent["patron"]):
                # Si encuentra una coincidencia, devuelve una respuesta aleatoria de las respuestas disponibles
                return random.choice(intent["respuesta"])  # Devuelve una respuesta aleatoria
        return None  # Si no se encuentra ninguna respuesta, retorna None

    def add_knowledge(self, question, answer, tag="nuevo"):
        """Agrega un nuevo intent o una respuesta a un intent existente."""
        for intent in self.intents:  # Recorre todos los intents cargados
            # Si ya existe un intent que contiene la pregunta, agrega la nueva respuesta
            if question.lower() in [p.lower() for p in intent["patron"]]:
                intent["respuesta"].append(answer)  # Añade la nueva respuesta al intent
                return  # Sale de la función sin guardar el archivo aún

        # Si no existe un intent con la pregunta, crea un nuevo intent con la pregunta y respuesta proporcionadas
        new_intent = {
            "tag": tag,  # El tag del intent (por defecto es "nuevo")
            "patron": [question],  # La lista de patrones (en este caso, solo una pregunta)
            "respuesta": [answer],  # La lista de respuestas (en este caso, solo una respuesta)
            "context_set": ""  # Se puede agregar más lógica para el contexto si es necesario
        }
        self.intents.append(new_intent)  # Agrega el nuevo intent a la lista de intents

    def save(self):
        """Guardar los cambios de la base de conocimiento solo cuando sea necesario."""
        self.save_knowledge()  # Llama al método para guardar los cambios en el archivo JSON


class SimpleChat:
    def __init__(self):
        """Inicializa el chat y la base de conocimientos."""
        self.kb = KnowledgeBase()  # Crea una nueva instancia de la clase KnowledgeBase

    def start_chat(self):
        """Inicia el chat con el usuario."""
        print("Chat: Hola! ¿En qué puedo ayudarte hoy?")  # Muestra el mensaje inicial del chat
        while True:  # Inicia un bucle para mantener el chat activo
            user_input = input("Tú: ")  # Obtiene la entrada del usuario
            # Comando para finalizar el chat
            if user_input.lower() in ["salir", "adiós", "chao"]:
                print("Chat: ¡Adiós! ¡Hasta luego!")  # Muestra el mensaje de despedida
                self.kb.save()  # Guarda los cambios antes de finalizar el chat
                break  # Termina el bucle y finaliza el chat

            response = self.kb.get_answer(user_input)  # Busca una respuesta para la entrada del usuario
            if response:  # Si se encuentra una respuesta
                print(f"Chat: {response}")  # Muestra la respuesta del chat
            else:
                print("Chat: No sé la respuesta a eso. ¿Podrías decirme qué debería responder?")  # Si no se encuentra respuesta
                new_response = input("Tú (nueva respuesta): ")  # Pide una nueva respuesta al usuario
                self.kb.add_knowledge(user_input, new_response)  # Agrega la nueva respuesta a la base de conocimientos
                self.kb.save()  # Guarda los cambios después de agregar el nuevo conocimiento
                print("Chat: ¡Gracias! He aprendido algo nuevo.")  # Agradece al usuario por enseñar algo nuevo


if __name__ == "__main__":  # Si el script se ejecuta directamente
    chat = SimpleChat()  # Crea una instancia de la clase SimpleChat
    chat.start_chat()  # Inicia el chat
