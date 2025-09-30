# Fraud Inference Service

This is the backend microservice responsible for detecting fraudulent transactions. It is built with Python and FastAPI. This service will be called by the [`checkout-service`](https://github.com/ShrutiC-git/go-k8s-service-with-kustomize) and will return with a boolean indicating whether the transaction is fraudulent or not.

The service works as follows:
1.  On startup, it connects to a MinIO object storage instance.
2.  It downloads and loads a pre-trained machine learning model (`model.pkl`) from the `fraud-models` bucket. This model is generated and saved by the [fraud-trainer ML job](https://github.com/ShrutiC-git/python-ml-batchjob).
3.  It exposes an HTTP endpoint to receive transaction data. However this endpoint is not accessible from the internet, but only from within the K8s cluster.
4.  Our `checkout-service` will internally call this endpoint with the transaction amount. 
5.  It uses the loaded model to predict if the transaction is fraudulent based on the amount. 
6.  It returns a boolean (`true`/`false`) result.

## API Endpoint

> Note: This service is not externally exposed. However accessed through its `ClusterIP`.

### `GET /predict`

Performs a fraud prediction based on the transaction amount.

**Query Parameters:**

*   `amount` (float, required): The amount of the transaction.
  

**Example Request:**

```bash
curl "http://inference-service.services.svc.cluster.local/predict?amount=150"
```

**Example Response:**

```json
{
  "amount": 150,
  "is_fraud": false
}
```
