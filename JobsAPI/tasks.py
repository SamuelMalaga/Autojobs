from celery import shared_task
import subprocess
from django.http import JsonResponse
import json

@shared_task
def test_task():
    for i in range(10):
        print(f"teste {i}")

    return "Done"

@shared_task
def execute_FULLpublicJscraper_task(job_name, job_location, job_type):
    try:
        # Execute o script JavaScript.
        script_path = 'C:/Users/SamuelMendesMalaga/Documents/Autojobs/JParser/JScrapers/FULLpublicJscraper.js'
        result = subprocess.run(['node', script_path, '--job-name', job_name, '--job-location', job_location, '--job-type', job_type], capture_output=True, text=True)

        # Verifique a saída do processo.
        if result.returncode == 0:
            # Retorne os dados relevantes como um dicionário
            return {'message': 'Script executado com sucesso', 'output': result.stdout}
        else:
            # Retorne os dados relevantes como um dicionário
            return {'message': 'Erro na execução do script', 'error_output': result.stderr}

    except Exception as e:
        # Retorne os dados relevantes como um dicionário
        return {'message': 'Erro na execução do script', 'error_message': str(e)}
