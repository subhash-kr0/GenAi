
![Screenshot 2023-03-06 125657](https://user-images.githubusercontent.com/104005791/223046037-4515954c-932c-40be-91dc-94fe1605478a.png)

# 1. What is AWS App Runner ?
AWS App Runner is a fully managed service that makes it easy to build and deploy containerized applications quickly and easily. It automates the entire build, deploy, and run workflows for containerized applications, making it simple to launch and scale containerized applications on AWS.

With App Runner, you can easily deploy your code from a source code repository or a container image stored in a container registry. App Runner builds and runs your application with fully managed compute and serverless infrastructure, so you don't have to worry about the underlying infrastructure. It also supports automatic scaling of your application based on traffic and demand, making it ideal for web applications, APIs, and microservices.

App Runner integrates with other AWS services, such as Amazon CloudWatch for logging and monitoring, AWS Identity and Access Management (IAM) for access control, and AWS CodePipeline for continuous integration and delivery.

In summary, AWS App Runner provides a simple and fast way to deploy containerized applications on AWS, without having to manage the underlying infrastructure.


# How to deploy our python project to aws app runner?

- ## So we have a python code which we'll dockerize and then deploy to `aws app runner service`

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    data = {'message': 'Hello, World!'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port= 5000)
    
```

> This is our `app.py` which is basically a `flask` app. 

- ## We have a requirements.txt which looks like - 

```txt
Flask==2.2.3
```
> So we have only one requirement for this project which is flask. You might have some other requiremtnts too, that's fine. 

- ## Let's have a look in the `Dockerfile`
```docker
FROM python:3.8.5-slim-buster

WORKDIR /app

COPY . /app


RUN pip install -r requirements.txt

CMD ["python3", "app.py"]

```

- ## We have a github workflow yml file which looks like the following 

```yml
name: workflow

on:
  push:
    branches:
      - main
    paths-ignore:
      - 'README.md'

permissions:
  id-token: write
  contents: read

jobs:
  integration:
    name: Continuous Integration
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Lint code
        run: echo "Linting repository"

      - name: Run unit tests
        run: echo "Running unit tests"

  build-and-push-ecr-image:
    name: Continuous Delivery
    needs: integration
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_DEFAULT_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          IMAGE_TAG: latest
        run: |
          # Build a docker container and
          # push it to ECR so that it can
          # be deployed to ECS.
          docker build -t ${{ secrets.AWS_ECR_REPO_URI }}:$IMAGE_TAG .
          docker push ${{ secrets.AWS_ECR_REPO_URI }}:$IMAGE_TAG

```
This GitHub Actions YAML file is a workflow for continuous integration and continuous delivery (CI/CD) pipeline. The workflow is triggered when code is pushed to the main branch, except for changes made to the README.md file.

The workflow has two jobs - integration and build-and-push-ecr-image. The integration job runs on an Ubuntu machine and checks out the code, runs a code linting process, and executes unit tests.

The build-and-push-ecr-image job is dependent on the integration job and runs on an Ubuntu machine. It checks out the code, configures AWS credentials, logs into Amazon ECR, builds and tags a Docker image with the latest tag, and pushes the image to an Amazon ECR repository specified in the secrets.

To authenticate with AWS, the workflow uses secrets for AWS access key ID, AWS secret access key, and AWS default region which should have to be stored in github repo secrets. The workflow also uses the aws-actions GitHub Actions to configure AWS credentials and login to Amazon ECR.

Overall, this workflow sets up a complete CI/CD pipeline for building, testing, and deploying code to Amazon ECR.

- ## You also need to create an `ECR repository` in aws and set the environment variable as `AWS_ECR_REPO_URI` in `github secrets`. 

> *make sure you have IAM access of - `AWSAppRunnerFullAccess` and `AmazonEC2ContainerRegistryFullAccess` so that you can access the `aws app runner` and `ecr repository`

### So, how to create an ECR repository? 

-  Go to your aws console and go to `Elastic container registry`
-  Click on `Crete repository`

    ![image](https://user-images.githubusercontent.com/104005791/223433858-22786a2d-0067-4f09-bc6a-8c10a77536cf.png)


-  Give it a suitable name.
  
    ![image](https://user-images.githubusercontent.com/104005791/223434131-ace5ead9-f78a-4212-a7e7-63e5d6071f03.png) 

- **Create The repository**

- Copy the repository url and save it to any notebook, we have to set the github secret with this.

  **To copy the repository url** -
  go to ECR home page then follow the below Screenshot. 

  ![image](https://user-images.githubusercontent.com/104005791/223434277-99a2d866-3b7d-47c3-aa88-54f131a3dd50.png)

- ## Now let's create `github secrets`. Check the `github action yml file` for secrets. 
For us, the yml file has three secrets which are 


- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
- `AWS_ECR_REPO_URI`

First two secrets you'll get when you'll get the credentials from aws IAM service.
set AWS_DEFAULT_REGION as `us-east-1` in secrets and the last one is our ECR repo url that we've just copied. 

> **To set the environment variables in github secrets, below are the steps**
- Go to your `github repository settings`

  ![image](https://user-images.githubusercontent.com/104005791/223434506-215add6c-63f9-4341-8351-ef1809f9fe68.png)

   ![image](https://user-images.githubusercontent.com/104005791/223434719-4eb98b0d-c2fd-4c0d-bb94-57b16d0f2372.png)

  ![image](https://user-images.githubusercontent.com/104005791/223434826-20c2ebc7-d880-4c4d-bdc4-dd402b27f2fb.png)

  ![image](https://user-images.githubusercontent.com/78023847/223423952-86a6e030-757e-4462-8ebd-a056f44d70d6.png)

- **Add the secret variable name in `Name` and set the value as in `secret` field** 

  ![image](https://user-images.githubusercontent.com/104005791/223424101-835f425b-dd08-4dcb-b370-243c3b07fc0d.png)

  >### For this case we are setting the `AWS_ECR_REPO_URI`. We will set the value as the url we copied from the ECR page. 

**Similarly We have to add the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and set the `AWS_DEFAULT_REGION` as `us-east-1`**

**Now if we have completed till this part, if our project is deployed to ECR, you can see the docker image file in your ECR repo. Now, here's the most interesting and important part. Let's create an `AWS APP RUNNER SERVICE`. How to do that? let's see.**


# Create a `AWS App Runner` service in AWS
 > First, sign in to your aws account. 



![image](https://user-images.githubusercontent.com/104005791/223048687-0052f9d3-c3f7-4537-bf33-47ebe01d5db3.png)

![image](https://user-images.githubusercontent.com/104005791/223049023-b457dc21-4afc-4fbd-9366-c2f5f9b69085.png)

![image](https://user-images.githubusercontent.com/104005791/223049179-c3062a41-9621-46cb-a48d-500e6a3d3223.png)

- ## Create the `App runner service`

![0001](https://user-images.githubusercontent.com/104005791/223429725-7bad7a58-7a99-47ec-862f-591c4a4e1827.jpg)

![0002](https://user-images.githubusercontent.com/104005791/223429970-c70ed3cd-55a8-4f83-b867-83f09cea71d0.jpg)

![0003](https://user-images.githubusercontent.com/104005791/223429994-f24e9465-748d-4190-864e-b12a8a0e0d77.jpg)

![0004](https://user-images.githubusercontent.com/104005791/223430007-b4a7c82d-2566-42a8-8305-99a5ed9a2af3.jpg)

![0005](https://user-images.githubusercontent.com/104005791/223430050-afe0173a-285b-473d-affe-258052e13199.jpg)
***N.B* - For our project, we will set the port as `5000`**
![0006](https://user-images.githubusercontent.com/104005791/223430081-db66407e-6fc8-4bf5-9d0b-4238bb605ea0.jpg)

![0007](https://user-images.githubusercontent.com/104005791/223430089-db5efa7d-5c68-4b64-8ead-01c742957284.jpg)



![image](https://user-images.githubusercontent.com/104005791/223431359-a35306dd-7828-4d80-8f87-b4789578b94e.png)

# Finally our project is deployed and the project/app could be accessed with the url we got from the step before.


### Let's suppose you want to delete the ECR repo and the App runner service? How to that? Let's see...


-  ## To delete the ECR repo follow the steps below

![image](https://user-images.githubusercontent.com/104005791/224032871-37d4c120-3d0e-4536-bb38-27610d765300.png)

![HowtoDeleteanAmazonECRRepository_PDF_2023-03-09130825 246201_page-0002](https://user-images.githubusercontent.com/104005791/224033750-fb128507-6bda-440d-893b-6a74d1d9eb51.jpg)

![HowtoDeleteanAmazonECRRepository_PDF_2023-03-09130825 246201_page-0003](https://user-images.githubusercontent.com/104005791/224033757-ccffc28f-3f2c-42f3-9a40-c2c72639b10e.jpg)


- ## Now you must be thinking how to delete the `Aws app runner service`, let's see how to do that

> Follow the steps below to delete an `app runner service`


![image](https://user-images.githubusercontent.com/104005791/224038137-ad7d0b79-00b7-4532-9042-d5a6c6cd4713.png)

![HowtoDeleteanAWSAppRunnerDemo_PDF_2023-03-09132919 040419_page-0002](https://user-images.githubusercontent.com/104005791/224039150-2993509a-3c24-40b3-b86d-df1b5408cd42.jpg)

![HowtoDeleteanAWSAppRunnerDemo_PDF_2023-03-09132919 040419_page-0003](https://user-images.githubusercontent.com/104005791/224039138-ff22352f-5b2f-477d-ba62-ca67b7b919f2.jpg)
![HowtoDeleteanAWSAppRunnerDemo_PDF_2023-03-09132919 040419_page-0004](https://user-images.githubusercontent.com/104005791/224039145-15e84c5a-2706-4d1b-878c-9048a0dcc15d.jpg)



> ## So we have deleted the `ECR` and `AWS APP RUNNER` services.










