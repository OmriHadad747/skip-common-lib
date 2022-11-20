from bson.codec_options import TypeEncoder, TypeRegistry, CodecOptions
from skip_db_lib.models.job import JobCategoryEnum, JobStatusEnum
from skip_db_lib.models.freelancer import FreelancerStatusEnum


class JobCategoryEncoder(TypeEncoder):

    python_type = JobCategoryEnum  # the Python type acted upon by this type codec

    def transform_python(self, value):
        """
        Function that transforms a custom type value into a type
        that BSON can encode.
        """
        return value.value


class JobStatusEncoder(TypeEncoder):

    python_type = JobStatusEnum  # the Python type acted upon by this type codec

    def transform_python(self, value):
        """
        Function that transforms a custom type value into a type
        that BSON can encode.
        """
        return value.value


class FreelancertatusEncoder(TypeEncoder):

    python_type = FreelancerStatusEnum  # the Python type acted upon by this type codec

    def transform_python(self, value):
        """
        Function that transforms a custom type value into a type
        that BSON can encode.
        """
        return value.value


job_category_encoder = JobCategoryEncoder()
job_status_encoder = JobStatusEncoder()
freelancer_status_encoder = FreelancertatusEncoder()
type_registry = TypeRegistry([job_category_encoder, job_status_encoder, freelancer_status_encoder])
codec_options = CodecOptions(type_registry=type_registry)
