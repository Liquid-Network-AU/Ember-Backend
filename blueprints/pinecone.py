from flask import Blueprint, request, jsonify
import pinecone

pinecone_api = Blueprint('pinecone_api', __name__)

# Initialize Pinecone client
pinecone_api.client = pinecone.Client(api_key='your-pinecone-api-key', environment='your-environment')

@pinecone_api.route('/pinecone/search', methods=['POST'])
def pinecone_search():
    try:
        data = request.json
        query = data.get('query')
        num_results = data.get('num_results', 10)

        # Perform a Pinecone similarity search
        response = pinecone_api.client.query(
            index_name='your-index-name',
            query={"query": query, "top_k": num_results}
        )

        results = [{"id": item.id, "score": item.score} for item in response.results]

        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pinecone_api.route('/pinecone/upsert', methods=['POST'])
def pinecone_upsert():
    try:
        data = request.json
        items = data.get('items')

        # Upsert data into Pinecone index
        pinecone_api.client.upsert(
            index_name='your-index-name',
            ids=[item['id'] for item in items],
            embeddings=[item['embedding'] for item in items]
        )

        return jsonify({"message": "Upsert successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pinecone_api.route('/pinecone/delete', methods=['POST'])
def pinecone_delete():
    try:
        data = request.json
        ids_to_delete = data.get('ids')

        # Delete data from Pinecone index
        pinecone_api.client.delete(
            index_name='your-index-name',
            ids=ids_to_delete
        )

        return jsonify({"message": "Delete successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500