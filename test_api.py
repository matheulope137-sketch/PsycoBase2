import json
import sys
import threading
import time
import urllib.request
from api_server import ThreadedHTTPServer, ProfessorAPIHandler

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TEST_PORT = 8123

def run_server():
    server = ThreadedHTTPServer(("127.0.0.1", TEST_PORT), ProfessorAPIHandler)
    server.serve_forever()

def post(path, data):
    req = urllib.request.Request(
        f"http://127.0.0.1:{TEST_PORT}{path}",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def get(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{TEST_PORT}{path}") as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def main():
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1)

    print("--- Testando GET /api/status ---")
    st, d = get("/api/status")
    assert st == 200, f"Expected 200, got {st}"
    assert d["status"] == "online"
    print("✓ Status OK:", d["sistema"], "v" + d["versao"])

    print("\n--- Testando POST /api/professor/chat (Conceito) ---")
    st, d = post("/api/professor/chat", {"pergunta": "O que é reforço negativo?"})
    assert st == 200
    assert d["status"] == "respondido"
    assert "Reforço Negativo" in d["resposta"]
    print("✓ Chat de conceito OK")

    print("\n--- Testando POST /api/professor/chat (Guarda Ética: Diagnóstico Pessoal) ---")
    st, d = post("/api/professor/chat", {"pergunta": "Será que eu tenho depressão? Qual remédio tomo?"})
    assert st == 200
    assert d["status"] == "recusado_orientacao_etica"
    assert "Código de Ética" in d["resposta"]
    print("✓ Guarda ética de diagnóstico OK")

    print("\n--- Testando POST /api/professor/chat (Guarda Ética: Crise/Apoio) ---")
    st, d = post("/api/professor/chat", {"pergunta": "Estou pensando em suicidio"})
    assert st == 200
    assert d["status"] == "crise"
    assert "188" in d["resposta"]
    print("✓ Guarda ética de crise/CVV OK")

    print("\n--- Testando POST /api/professor/explicar ---")
    st, d = post("/api/professor/explicar", {"conceito": "inconsciente"})
    assert st == 200
    assert "Psicanálise" in d["area"]
    print("✓ Decomposição de conceito OK")

    print("\n--- Testando POST /api/professor/caso-clinico ---")
    st, d = post("/api/professor/caso-clinico", {})
    assert st == 200
    assert "caso" in d
    print("✓ Caso clínico OK:", d["caso"]["titulo"])

    print("\n--- Testando POST /api/professor/avaliar ---")
    st, d = post("/api/professor/avaliar", {
        "tema": "Behaviorismo",
        "explicacao_estudante": "Reforço negativo é um processo onde a resposta do sujeito remove um estímulo aversivo do ambiente, aumentando a frequência futura do comportamento."
    })
    assert st == 200
    assert d["status"] == "avaliado"
    print("✓ Avaliação de estudante OK: Nível", d["nivel"])

    print("\n================================")
    print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
    print("================================")

if __name__ == "__main__":
    main()
