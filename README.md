# vikashyadav-introtoaws-jtu23
This is my assignment for AWS track of jTU-23

----
## **Final Output:**

Upload an image to `images` folder in the source bucket, and see the thumbnails automatically getting generated in the `thumbnails` folder in destination bucket in 3 different sizes. `ImageProcessor` (a lambda function) does it automatically for you.

> To access the `source bucket`, click here: [vikashyadav-source](https://s3.console.aws.amazon.com/s3/buckets/vikashyadav-source?region=us-east-1)<br>
> To access the `destination bucket`, click here: [vikashyadav-destination](https://s3.console.aws.amazon.com/s3/buckets/vikashyadav-destination?region=us-east-1)

(_if the links don't work, go to aws s3, and search for the bucket names instead to access my buckets_)

>  Go here to subscibe to the `imageprocessor notifications` (via email): [Visit this page](http://vikashyadav-introtoaws-cloudfront-dist.s3-website-us-east-1.amazonaws.com/) (Bonus milestone)

(_You will receive a confirmation link on your email, confirm to get subscribed to notifications of my lambda._)

----
## **Resources:**

I have used multiple AWS resources to achieve this. Here are is the list of all resources:

### S3 Buckets:

> `vikashyadav-source s3 Bucket`:
Here you upload your image (in the images folder).
Link: [vikashyadav-source](https://s3.console.aws.amazon.com/s3/buckets/vikashyadav-source?region=us-east-1)
![Image](https://user-images.githubusercontent.com/132905581/239720104-9ca64784-b868-4cf7-8836-5aeb5c6a052f.png)

> `vikashyadav-destination Bucket`:
Here the thumbnails get generated automatically (in the thumbnails folder).
Link: [vikashyadav-destination](https://s3.console.aws.amazon.com/s3/buckets/vikashyadav-destination?region=us-east-1)
![Image](https://user-images.githubusercontent.com/132905581/239720170-91e1511d-e3c0-42f7-858a-ed7d4058b597.png)

### IAM:

> `vikashyadav-introtoaws role`:
This is a role that my lambda function and SNS topic assume.
Link: [vikashyadav-introtoaws](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/roles/details/vikashyadav-introtoaws)
![Image](https://user-images.githubusercontent.com/132905581/239720440-6f79263c-dbb6-4960-8477-7d4966fe7aa3.png)
It's trust relationships:
![Image](https://user-images.githubusercontent.com/132905581/239720451-9c168ce2-ff1a-43c0-83bd-6af9ed9e1036.png)
It has 2 policies attached:
![Image](https://user-images.githubusercontent.com/132905581/239720463-77227871-cd0e-405b-887f-faafb1b3f4a6.png)

> `vikashyadav-introtoaws policy`:
This policy gives permissions to access the above 2 buckets, to publish or subscribe to my sns topic (for notifications part) and full access to CloudWatch logs.
Link: [vikashyadav-introtoaws](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/policies/details/arn%3Aaws%3Aiam%3A%3A280022023954%3Apolicy%2Fvikashyadav-introtoaws)
![Image](https://user-images.githubusercontent.com/132905581/239720620-02d60c44-6b4e-4d9e-8ff4-652c151ff30c.png)
It's permissions:
![Image](https://user-images.githubusercontent.com/132905581/239720564-2d73d511-df5d-4ee3-a457-912f7868afdf.png)

### Lambdas:

> `vikashyadav-imageprocessor lambda function`:
This gets triggered whenenver there is a new object in source buckets' image folder and automatically generates the thumbnails (in 3 sizes) and stores them to thumbnails folder in destionation bucket. It also publishes the update to the SNS topic.
Link: [vikashyadav-imageprocessor](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/vikashyadav-imageprocessor)
![Image](https://user-images.githubusercontent.com/132905581/239720749-defad671-b83d-4324-af04-2d3d85f126ff.png)
It's trigger:
![Image](https://user-images.githubusercontent.com/132905581/239720767-9af9055c-04ff-40d7-aa21-1ad9cfb27484.png)
It uses one layer for the PIL library

### SNS:

> `vikashyadav-introtoaws sns topic`:
Used this for notifications. Anyone can subscribe to this topic, but only the vikashyadav-introtoaws role can publish to this topic.
Link: [vikashyadav-introtoaws](https://us-east-1.console.aws.amazon.com/sns/v3/home?region=us-east-1#/topic/arn:aws:sns:us-east-1:280022023954:vikashyadav-introtoaws)
![Image](https://user-images.githubusercontent.com/132905581/239720944-86632465-b283-44b8-a73d-443731dbc67c.png)
Access Policy:
![Image](https://user-images.githubusercontent.com/132905581/239720988-67fc4e85-4c5d-4c02-a0b9-274776a10ff4.png)
![Image](https://user-images.githubusercontent.com/132905581/239720993-8cdb01d9-7972-4e36-a9f3-ddc9f8f835a1.png)

### Webpage:

> `vikashyadav-introtoaws-cloudfront-dist s3bucket`:
An s3 bucket to host my webpage. The webpage allows you to subscibe to the SNS topic.
Link: [vikashyadav-introtoaws-cloudfront-dist](https://s3.console.aws.amazon.com/s3/buckets/vikashyadav-introtoaws-cloudfront-dist?region=us-east-1)
![Image](https://user-images.githubusercontent.com/132905581/239721097-93ea10ec-a73a-43e8-93bd-91b9a9f4014d.png)
Hosting (using cloudfront):
![Image](https://user-images.githubusercontent.com/132905581/239721119-0b8e3b5e-fed3-4986-a1e0-277df3ae6978.png)
Link to webpage: [click here](http://vikashyadav-introtoaws-cloudfront-dist.s3-website-us-east-1.amazonaws.com)

> `vikashyadav-introtoaws Cognito Identity Pool`:
This identity pool was needed to temporarily authorize AWS javascript SDK on my webpage to be able to subscibe to the SNS topic.
Link: [Find it on this page with the name vikashyadav-introtoaws](https://us-east-1.console.aws.amazon.com/cognito/federated?region=us-east-1)
![Image](https://user-images.githubusercontent.com/132905581/239721365-ff7e2d0a-6202-4701-aaf3-9dd90f4e081a.png)
It also needed new roles with very limited access (just to subscribe to the topic).
These roles are [-Cognito_vikashyadavintrotoawsAuth_Role](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/roles/details/-Cognito_vikashyadavintrotoawsAuth_Role) and [-Cognito_vikashyadavintrotoawsUnauth_Role](https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/roles/details/-Cognito_vikashyadavintrotoawsUnauth_Role)
These roles have this permission:
![Image](https://user-images.githubusercontent.com/132905581/239721465-459f4d7a-b57d-41c3-83c6-d46aafc68cb6.png)







