from sagemaker import get_execution_role
import sagemaker as sage
from sagemaker.estimator import Estimator

role = get_execution_role()
sess = sage.Session()

account = sess.boto_session.client('sts').get_caller_identity()['Account']
region = sess.boto_session.region_name
image = '{}.dkr.ecr.{}.amazonaws.com/sm-tf-horovod:latest'.format(account, region)

job_name = "test_job_2"

output_base = "s3://thangakr-sm-east1/mnist_out"
output_discard = output_base + "/discard"
tensorboard_base = output_base + "/tensorboard"
tensorboard_log_path = tensorboard_base + "/" + job_name
output_path = output_base + "/model/" + job_name
#output_path = "s3://{}/output".format(sess.default_bucket())

hyperparams = {"sagemaker_submit_directory":"s3://thangakr-sm-east1/mnist_code.tar.gz",
              "sagemaker_region":'"us-east-1"',
              "sagemaker_job_name":"first_job",
              "sagemaker_program":"tensorflow_mnist_estimator.py",
              "sagemaker_use_mpi":"True",
              "tensorboard_log_path":tensorboard_log_path,
              "output_path":output_path,
              "sagemaker_use_tmpfs":"True",
              "sagemaker_tmpfs_size":"4"}

estimator = Estimator(image, role=role, output_path=output_discard,
                      train_instance_count=1,
                      train_instance_type='ml.p2.8xlarge',
                      sagemaker_session=sess,
                      hyperparameters=hyperparams,
                      train_volume_size=128)

estimator.fit("s3://thangakr-sm-east1/mnist_data/")
