import boto3, time


#get instance 
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')
INSTANCE_ID = "i-0df469dd2ac613ae6"

ssm_full_ctl = {"IamInstanceProfile":{'Arn': "arn:aws:iam::780988366548:instance-profile/SSM_EC2_CTL",'Name': 'SSM_EC2_CTL' },"InstanceId":INSTANCE_ID}
#add instance profile 

def assign_ssm_iam_role():
        ec2.associate_iam_instance_profile(**ssm_full_ctl)

def execute_ssm_document():
   kwargs = {"InstanceIds":[INSTANCE_ID],"DocumentName":"updateAndInstallChefWs"}

   res = ssm.send_command(**kwargs)
   time.sleep(5)
   return res.get('Command').get('CommandId')


def verfify_cmd_status():

    cid = execute_ssm_document()

    args = {"CommandId": cid, "InstanceId": INSTANCE_ID}

    response = ssm.get_command_invocation(**args)

   
    while True: 
        
        response = ssm.get_command_invocation(**args)
        print(response.get('Status'))
        
        if response.get('Status') == 'Success' or response.get('Status') == 'Failed':
            if 'Loaded plugins' in response.get('StandardOutputContent'):
                print('Actually this command executed Successfully')
                print('\n\n\n\n')
                print(response)
                break
            else:
                print(response)
                break


if __name__ == "__main__":

    try:
        assign_ssm_iam_role()
    except Exception as e:
        print(e)
    verfify_cmd_status()