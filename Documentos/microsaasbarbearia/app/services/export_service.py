import csv
import io
from app.models.client import Client


def export_clients_csv(clients):
    """Gera CSV com lista de clientes."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Nome", "Telefone", "Email", "CPF", "Visitas", "Criado em"])

    for c in clients:
        writer.writerow([
            c.name,
            c.phone or "",
            c.email or "",
            c.cpf or "",
            c.visits_count,
            c.created_at.strftime("%d/%m/%Y"),
        ])

    output.seek(0)
    return output.getvalue()
