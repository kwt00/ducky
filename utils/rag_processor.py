import requests
import json

def process_rag(folder_path, index_folder=None):
    # Since Vectara API is being used directly, we may not need to process documents here.
    # However, if you need to upload documents to Vectara, implement that logic here.
    pass  # Placeholder for any preprocessing if needed

def answer_question(question, index_folder=None):
    url = "https://api.vectara.io:443/v2/query"

    headers = {
        "customer-id": "2928622251",
        "Content-Type": "application/json",
        "Authorization": (
            "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0NGE4NTA5LTM3MTUtNGUyYy1hNjZmLWYyMGZmZTc4NmE1MyIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcl9pZCI6MjkyODYyMjI1MSwiZXhwIjoxNzI5NDYzMzcwLCJpYXQiOjE3Mjk0NTk3NzAsImlzcyI6Imh0dHBzOi8vY29vbC12aXN2ZXN2YXJheWEtaWdkaG82N3UwMy5wcm9qZWN0cy5vcnlhcGlzLmNvbSIsImp0aSI6IjBiODNkMTJjLThlZjgtNGJlOS04NGE4LWI0Nzc1OTA4MTc2MyIsIm5iZiI6MTcyOTQ1OTc3MCwic2NoZW1hX2lkIjoiMTRlNjE0ZTA3ZjExMzU5MzZhMmZmNjk0ZDljZDFlMGU1OGQ4ZmY0ZGM0Y2UyMWI5ZWJiMDJlNWU0MmRkMDcyYzdlYzVhYTE4NDVmYmYzOWVhOWQ4YTVjZjRkNmU4ODE3MzM2OGM2MzU1YjhhZGFhMTg5OTM1OTI2MWY0MDAyOTciLCJzZXNzaW9uIjp7ImFjdGl2ZSI6dHJ1ZSwiYXV0aGVudGljYXRlZF9hdCI6IjIwMjQtMTAtMjBUMTk6MDU6MjcuNTY3MTA4WiIsImF1dGhlbnRpY2F0aW9uX21ldGhvZHMiOlt7ImFhbCI6ImFhbDEiLCJjb21wbGV0ZWRfYXQiOiIyMDI0LTEwLTIwVDE5OjA1OjI3LjU2NzAxNTI5OFoiLCJtZXRob2QiOiJvaWRjIiwicHJvdmlkZXIiOiJnb29nbGUifV0sImF1dGhlbnRpY2F0b3JfYXNzdXJhbmNlX2xldmVsIjoiYWFsMSIsImRldmljZXMiOlt7ImlkIjoiMzhjZTI2MzgtMDlhYi00NzQwLWE0MWQtZjAxOTkzNDA5NzYyIiwiaXBfYWRkcmVzcyI6IjEzNS4xODAuMzcuMTI1IiwibG9jYXRpb24iOiJTYW4gRnJhbmNpc2NvLCBVUyIsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTI5LjAuMC4wIFNhZmFyaS81MzcuMzYifV0sImV4cGlyZXNfYXQiOiIyMDI0LTEwLTIzVDE5OjA1OjI3LjU2NzAxNVoiLCJpZCI6IjNlMDFlYTg1LTcwY2ItNDc2ZS1iYTYzLTQ1ZGFkZWU1YmI1NSIsImlkZW50aXR5Ijp7ImNyZWF0ZWRfYXQiOiIyMDI0LTEwLTIwVDE5OjA1OjI3LjA3MzE4N1oiLCJpZCI6ImE5NDM4NDdjLWU3NmYtNDNmZi05OGNjLTZkZTcwN2JjYTVmOCIsIm1ldGFkYXRhX3B1YmxpYyI6bnVsbCwib3JnYW5pemF0aW9uX2lkIjpudWxsLCJzY2hlbWFfaWQiOiIxNGU2MTRlMDdmMTEzNTkzNmEyZmY2OTRkOWNkMWUwZTU4ZDhmZjRkYzRjZTIxYjllYmIwMmU1ZTQyZGQwNzJjN2VjNWFhMTg0NWZiZjM5ZWE5ZDhhNWNmNGQ2ZTg4MTczMzY4YzYzNTViOGFkYWExODk5MzU5MjYxZjQwMDI5NyIsInNjaGVtYV91cmwiOiJodHRwczovL2Nvb2wtdmlzdmVzdmFyYXlhLWlnZGhvNjd1MDMucHJvamVjdHMub3J5YXBpcy5jb20vc2NoZW1hcy9NVFJsTmpFMFpUQTNaakV4TXpVNU16WmhNbVptTmprMFpEbGpaREZsTUdVMU9HUTRabVkwWkdNMFkyVXlNV0k1WldKaU1ESmxOV1UwTW1Sa01EY3lZemRsWXpWaFlURTRORFZtWW1Zek9XVmhPV1E0WVRWalpqUmtObVU0T0RFM016TTJPR00yTXpVMVlqaGhaR0ZoTVRnNU9UTTFPVEkyTVdZME1EQXlPVGMiLCJzdGF0ZSI6ImFjdGl2ZSIsInN0YXRlX2NoYW5nZWRfYXQiOiIyMDI0LTEwLTIwVDE5OjA1OjI3LjA3MTI2N1oiLCJ0cmFpdHMiOnsiZW1haWwiOiJrZXZpbi50YXlsb3IxOTI0QGdtYWlsLmNvbSIsInVzZXJfaW5mbyI6eyJjdXN0b21lcl9pZCI6MjkyODYyMjI1MSwidXNlcm5hbWUiOiJrZXZpbi50YXlsb3IxOTI0QGdtYWlsLmNvbSJ9fSwidXBkYXRlZF9hdCI6IjIwMjQtMTAtMjBUMTk6MDY6NDEuMzU4NzYzWiJ9LCJpc3N1ZWRfYXQiOiIyMDI0LTEwLTIwVDE5OjA1OjI3LjU2NzAxNVoifSwic2lkIjoiM2UwMWVhODUtNzBjYi00NzZlLWJhNjMtNDVkYWRlZTViYjU1Iiwic3ViIjoiYTk0Mzg0N2MtZTc2Zi00M2ZmLTk4Y2MtNmRlNzA3YmNhNWY4In0.dSpoGniO2zY74gPQ6l_Ak21U7jLrEebB3d-CyzE6A9AqoiEKXfYSTJHKIJJRovhfZM8GcPY590yCEC9lII62B0tiY1_dhkZyAeU8xbto7IL4ibRUAPkYWuX0XsgA_TPZoOG4Kn4Cbdt28KXlyFm4J5Sc6xmGCNbEC7mWa2Wgn3UGWMI-dHb68OwUri8Iywr5uQc1fFtWnD9ZxjJ_s-u8blwyi8JUMfG0ms3u5VJ6n1K1L2HxlvBLnazqZTUmSpSABkj3ioURGmNA4WVhQZFPBOjevOhbSGbZ3BY2fBTfGTcjfq5ajIedQA7wCaKeuRPS1r738KV33Fp7BS5sT4vIcVAIrLdKDFNaaQ9--Adwu1_ooQHzpj9yqBEX__YIJaizQ68TPQFKM3ujP_JeUEtVg6UN0w_QV9EE7bKAoV1txw6CMADHX3iG6KGHMyeG8xllYxGvrbi-BcR9EscUEHwB3E7ZqioT60F8GnM7LWLG7k4dUu0Bc8FVKU7GQy1YUmwTKPoBH4OJM37F5ZjkDa256KqNVjjNtnHIkRI3gDu5dr5ZfPX-2Ss4cliu3xNrb-3dZtPc4oINl5-h5vLZ0FgIqmYzUJPPfFHSp2kj9NTqRVUniWBepQpk71vS-S4nQc0EjFHPniFRKiIoF7g5bFKH14G3LFBxePTD2pMvvn9WsVY"
        ),
    }

    payload = {
        "query": question,
        "search": {
            "corpora": [{"corpus_key": "ducky", "metadata_filter": "", "lexical_interpolation": 0.005}],
            "offset": 0,
            "limit": 25,
            "context_configuration": {
                "sentences_before": 2,
                "sentences_after": 2,
                "start_tag": "%START_SNIPPET%",
                "end_tag": "%END_SNIPPET%"
            },
            "reranker": {"type": "mmr", "diversity_bias": 0}
        },
        "stream_response": False,
        "generation": {
            "generation_preset_name": "mockingbird-1.0-2024-07-16",
            "max_used_search_results": 5,
            "response_language": "eng",
            "enable_factual_consistency_score": True
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()
        summary = result.get('summary', "No summary found")
        return summary
    else:
        error_message = f"Error: {response.status_code} - {response.text}"
        print(error_message)
        return "Sorry, an error occurred while processing your question."