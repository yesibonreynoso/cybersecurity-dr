from pathlib import Path

from herramientas import build_answer


def main() -> None:
    document_path = Path("data/ciberseguridad.csv")
    print("Agente de ciberseguridad activo.")
    print("Escribe 'salir' para terminar.\n")

    while True:
        question = input("Pregunta: ").strip()
        if question.lower() in {"", "salir"}:
            break
        answer = build_answer(question, document_path)
        print(f"\nRespuesta:\n{answer}\n")


if __name__ == "__main__":
    main()
