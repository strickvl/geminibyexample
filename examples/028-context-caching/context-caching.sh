# Install the Google Generative AI library
$ pip install google-genai

# Run the Python script
$ python context-caching.py
Cache created with name: cachedContents/n8upgecthnz7
Cached token count: 107203
Cache expires at: 2025-04-05 20:21:48.818511+00:00
Query: What are the recommended use cases for ZenML's pipeline orchestration?
Total tokens: 107387
Cached tokens: 107203
Output tokens: 168
Response: ZenML's pipeline orchestration is well-suited for a wide range of machine learning workflows, including:
* **Data preprocessing:**  Ingesting, cleaning, transforming, and preparing data for model training.
* **Model training:**  Training various types of machine learning models, including deep learning models.
* **Model evaluation:**  Assessing model performance using different metrics and techniques.
* **Model deployment:**  Deploying trained models to different environments for inference.
* **Model monitoring:**  Monitoring the performance and health of deployed models in real-time.
* **A/B testing:**  Experimenting with different model variations and comparing their performance.
* **Hyperparameter tuning:**  Finding optimal hyperparameters for models.
* **Feature engineering:**  Developing and evaluating new features for improving model performance. 
...
Query: How does ZenML integrate with cloud providers?
Total tokens: 107326
Cached tokens: 107203
Output tokens: 113
Response: ZenML integrates with cloud providers by offering stack components that are specific to each provider, such as:
* **Artifact Stores:** S3 (AWS), GCS (GCP), Azure Blob Storage (Azure)
* **Orchestrators:** Skypilot (AWS, GCP, Azure), Kubernetes (AWS, GCP, Azure)
* **Container Registries:** ECR (AWS), GCR (GCP), ACR (Azure)
These components allow you to run pipelines on cloud infrastructure, enabling you to scale and leverage the benefits of cloud computing. 
...
