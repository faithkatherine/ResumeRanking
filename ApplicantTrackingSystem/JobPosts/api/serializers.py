from rest_framework import serializers
from JobPosts.models import JobPost
from django.contrib.auth.models import User

from django.core.files.base import ContentFile
import base64
import six
import uuid
import os
from django.conf import Settings, settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

from JobPosts.utils import is_image_aspect_ratio_valid, is_image_size_valid

class Base64ImageField(serializers.ImageField):
	def to_internal_value(self, data):

		# Check if this is a base64 string 
		if isinstance(data, six.string_types):
			# Check if the base64 string is in the "data:" format
			if 'data:' in data and ';base64,' in data:
				# Break out the header from the base64 content
				header, data = data.split(';base64,')

			# Try to decode the file. Return validation error if it fails.
			try:
				decoded_file = base64.b64decode(data)
			except TypeError:
				self.fail('invalid_image')

			# Generate file name:
			file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
			# Get the file name extension:
			file_extension = self.get_file_extension(file_name, decoded_file)

			complete_file_name = "%s.%s" % (file_name, file_extension, )

			data = ContentFile(decoded_file, name=complete_file_name)

			return super(Base64ImageField, self).to_internal_value(data)

	def get_file_extension(self, file_name, decoded_file):
		import imghdr

		extension = imghdr.what(file_name, decoded_file)
		extension = "jpg" if extension == "jpeg" else extension
		return extension
	
class JobPostSerializer(serializers.ModelSerializer):

	username = serializers.SerializerMethodField('get_username_from_author')
	image 	 = serializers.SerializerMethodField('validate_image_url')


	class Meta:
		model = JobPost
		fields = ['pk', 'title', 'slug', 'body', 'image', 'date_updated', 'username']


	def get_username_from_author(self, job_post):
		username = job_post.author.username
		return username

	def validate_image_url(self, job_post):
		image = job_post.image
		new_url = image.url
		if "?" in new_url:
			new_url = image.url[:image.url.rfind("?")]
		return new_url




class JobPostUpdateSerializer(serializers.ModelSerializer):
	#image = Base64ImageField(use_url=True)
	class Meta:
		model = JobPost
		fields = ['title', 'body', 'image']

	def validate(self, job_post):
			
		try:
			title = job_post['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			body = job_post['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
		
			image = job_post['image']
			url = os.path.join(settings.TEMP , str(image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()

			#Check image size
			#if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
			#	os.remove(url)
			#	raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			#if not is_image_aspect_ratio_valid(url):
			#	os.remove(image)
			#	raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			#	os.remove(url)
		except KeyError:
			pass
		return job_post


class JobPostCreateSerializer(serializers.ModelSerializer):


	class Meta:  
		model = JobPost
		fields = ['title', 'body', 'image', 'date_updated', 'author']


	def save(self):
		
		try:
			image = self.validated_data['image']
			title = self.validated_data['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			body = self.validated_data['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
			
			job_post = JobPost(
								author = self.validated_data['author'],
								title=title,
								body=body,
								image=image,
								)

			url = os.path.join(settings.TEMP, str(image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()

			# Check image size
			#if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
			#	os.remove(url)
			#	raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			#if not is_image_aspect_ratio_valid(url):
			#	os.remove(url)
			#	raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
			job_post.save()
			return job_post
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})