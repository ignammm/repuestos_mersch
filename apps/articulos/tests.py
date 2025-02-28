import os
import csv
import json
import http.client
from io import StringIO
from dotenv import load_dotenv
from django.test import TestCase
from .models import ArticuloRSF

load_dotenv()

def obtener_token():
    """Obtiene el token de autenticación de la API usando http.client."""
    conn = http.client.HTTPSConnection("plataformarsf.com", 1039)
    payload = json.dumps({
        "cuentaRSF": os.getenv("RSF_USER"),
        "password": os.getenv("RSF_PASS")
    })

    headers = {"Content-Type": "application/json"}

    try:
        conn.request("POST", "/api/Login", body=payload, headers=headers)
        response = conn.getresponse()
        raw_response = response.read().decode()
        print(f"🔎 Respuesta del servidor: {raw_response}")

        if response.status == 200:
            data = json.loads(raw_response)
            return data.get("accessToken", None)
        else:
            print(f"❗ Error: {response.status} - {response.reason}")
            return None

    except Exception as e:
        print(f"❌ Error al intentar obtener el token: {e}")
        return None
    finally:
        conn.close()


def do():
    """Realiza la solicitud a la API, procesa el CSV y guarda los datos en la base de datos."""
    load_dotenv()
    token = obtener_token()

    if token:
        conn = http.client.HTTPSConnection("plataformarsf.com", 1039)
        headers = {"Authorization": f"Bearer {token}"}

        try:
            conn.request("GET", "/api/Productos/Lista", headers=headers)
            response = conn.getresponse()

            if response.status == 200:
                # ✅ Procesar el archivo CSV
                csv_data = StringIO(response.read().decode())
                reader = csv.DictReader(csv_data)

                for item in reader:
                    ArticuloRSF.objects.update_or_create(
                        CodigoBarra=item.get('codigo_barras', None),
                        defaults={
                            'Articulo': item.get('nombre', None),
                            'MarcaOriginal': item.get('marca', None),
                            'TipoTxt': item.get('tipo', None),
                            'MarcaRSF': item.get('marca_rsf', None),
                            'Fabrica': item.get('fabrica', None),
                            'Descripcion': item.get('descripcion', None),
                            'PrecioLista': float(item.get('precio_lista', 0)) if item.get('precio_lista') else None,
                            'PrecioNeto': float(item.get('precio_neto', 0)) if item.get('precio_neto') else None,
                            'StockFinal': int(item.get('stock_final', 0)) if item.get('stock_final') else None,
                            'ModuloVenta': int(item.get('modulo_venta', 0)) if item.get('modulo_venta') else None,
                            'Rubro': item.get('rubro', None),
                            'Segmento': item.get('segmento', None),
                            'Enlace': item.get('enlace', None),
                            'OEM': item.get('oem', None),
                            'CodigoRSF': item.get('codigo_rsf', None),
                        }
                    )

                print("✅ Sincronización exitosa con la API del proveedor.")
            else:
                print(f"❗ Respuesta de la API: {response.status} - {response.reason}")

        except Exception as e:
            print(f"❌ Error al conectar con la API: {e}")
        finally:
            conn.close()
    else:
        print("❌ No se pudo obtener el token de autenticación.")
