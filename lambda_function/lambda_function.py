import boto3
from PIL import Image
import io
import logging


def publish_msg(msg,sub):
    # use the AWS SDK to publish a message to the SNS topic
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:280022023954:vikashyadav-introtoaws',
        Message=msg,
        Subject=sub
    )


def lambda_handler(event, context):

    # Set up logging
    logger = logging.getLogger()
    logging.basicConfig(format='%(levelname)s:%(message)s')
    logger.setLevel(logging.INFO)

    source_bucket = 'vikashyadav-source'
    source_key = event['Records'][0]['s3']['object']['key']
    destination_bucket = 'vikashyadav-destination'

    s3 = boto3.client('s3')

    try:
        # Download the original image
        logger.info(f'Downloading {source_bucket}/{source_key}')
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        image = Image.open(io.BytesIO(response['Body'].read()))

        sizes = [(64, 64), (128, 128), (256, 256)]

        # Generate thumbnails
        for thumbnail_size in sizes:
            logger.info(f'Generating thumbnail with size {thumbnail_size}')
            thumbnail = image.copy()
            thumbnail.thumbnail(thumbnail_size)

            # Create an in-memory stream to hold the thumbnail data
            thumbnail_stream = io.BytesIO()
            thumbnail.save(thumbnail_stream, format='PNG')
            thumbnail_stream.seek(0)

            # Upload the thumbnail to the destination bucket
            destination_key = source_key.split('/')[-1]
            name, extension = destination_key.split('.')
            destination_key = f'{name}_{thumbnail_size[0]}x{thumbnail_size[1]}.png'
            destination_key = f'thumbnails/{destination_key}'
            s3.put_object(Body=thumbnail_stream,
                          Bucket=destination_bucket, Key=destination_key)

            logger.info(
                f'Uploaded thumbnail to {destination_bucket}/{destination_key}')

        logger.info('Thumbnails generated and uploaded successfully')

        Message=f'Thumbnails generated successfully for {source_bucket}/{source_key}'
        Message+=f' and uploaded to {destination_bucket}/thumbnails/'
        Subject='ImageProcessor Lambda Triggered: Success!'
        
        try:
            publish_msg(Message,Subject)
            logger.info('Email for success sent successfully')
        except Exception as e:
            logger.error(f'Error sending success email: {str(e)}')

        return {
            'statusCode': 200,
            'body': 'Thumbnail generated and uploaded successfully'
        }

    except Exception as e:

        logger.error(f'Error generating or uploading thumbnail: {str(e)}')

        Message=f'Tried generating thumbnail for {source_bucket}/{source_key} and Failed.'
        Message+=f'Error in generating or uploading thumbnail: {str(e)}'
        Subject='ImageProcessor Lambda Triggered: Failed!'
        publish_msg(Message,Subject)

        try:
            publish_msg(Message,Subject)
            logger.info('Email for failure sent successfully')
        except Exception as e:
            logger.error(f'Error sending failure email: {str(e)}')

        return {
            'statusCode': 500,
            'body': f'Error generating or uploading thumbnail: {str(e)}'
        }
