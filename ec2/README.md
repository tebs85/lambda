# Lambda: EC2 Management

This module are Lambda functions that aim to automate SysAdmin function, to manage EC2 instances deployed in AWS. 


# Table of contents

1. `SSH EC2`    Using SSM to store the RSA Key, retrieves the key and then ssh into EC2 and runs shell commands.
2. `Start EC2`  Start selected, instances tagged with `autoManageInstanceSatus` with stop|start or all instances in region
3. `Stop EC2`   Stop selected, instances tagged with `autoManageInstanceSatus` with stop|start or all instances in region
