import json
import subprocess


def add_connections_from_json(file_path):
    with open(file_path, 'r') as file:
        connections = json.load(file)
        for conn_id, conn_details in connections.items():
            conn_type = conn_details.pop("conn_type")
            cmd = [
                "airflow", "connections", "add",
                conn_id,
                "--conn-type", conn_type
            ]
            for key, value in conn_details.items():
                cmd.extend([f"--conn-{key}", str(value)])
            subprocess.run(cmd)


add_connections_from_json('./connections.json')