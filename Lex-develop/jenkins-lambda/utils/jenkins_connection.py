# utils/jenkins_connection.py
import jenkins

USER = 'admin'
API = 'beb6e0bd78f5420eac396bd07dbd5093'
JENKINS_Url = "http://34.207.205.239:8080/"
server = jenkins.Jenkins(JENKINS_Url, username=USER, password=API)

def delete_job(jobname):
    """
    Deletes the specified Jenkins job.
    """
    if server.job_exists(jobname):
        server.delete_job(jobname)
    else:
        raise ValueError(f"Job '{jobname}' does not exist.")


