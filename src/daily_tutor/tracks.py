"""Certification / learning track presets.

Each track becomes a topic whose subtopics are the exam objectives, so get_coverage can
show which objectives are untouched. These are STUDY OUTLINES written from the publicly
known exam domains; always check the current official exam guide, vendors revise them.
(Items contain no commas on purpose.)
"""

TRACKS = {
    "ccna": {
        "name": "CCNA",
        "description": "Cisco CCNA 200-301: network fundamentals, access, IP connectivity, services, security, automation.",
        "objectives": [
            "OSI and TCP/IP models", "Switching and MAC learning", "VLANs and trunking", "STP and RSTP",
            "EtherChannel", "Wireless fundamentals", "IPv4 addressing and subnetting", "IPv6 addressing",
            "Static routing", "OSPF single area", "First-hop redundancy", "NAT and PAT", "DHCP and DHCP relay",
            "DNS and NTP", "SNMP and Syslog", "QoS basics", "ACLs", "Port security and L2 attacks",
            "VPN fundamentals", "REST APIs and JSON", "SDN and controller-based networking",
            "Ansible Puppet and Chef concepts",
        ],
    },
    "cka": {
        "name": "CKA",
        "description": "Certified Kubernetes Administrator: cluster setup, workloads, services, storage, troubleshooting.",
        "objectives": [
            "RBAC", "kubeadm install and upgrade", "etcd backup and restore", "Helm and Kustomize",
            "Deployments and rolling updates", "ConfigMaps and Secrets", "Scheduling: taints and affinity",
            "Resource requests and limits", "Services and endpoints", "Ingress and Gateway API",
            "NetworkPolicy", "CoreDNS", "PV PVC and StorageClasses", "Troubleshooting nodes",
            "Troubleshooting control plane", "Troubleshooting application networking", "Logs and monitoring",
        ],
    },
    "rhcsa": {
        "name": "RHCSA",
        "description": "Red Hat Certified System Administrator (EX200): essential tools, storage, services, users, security.",
        "objectives": [
            "Shell redirection grep and regex", "tar gzip and archives", "systemd units and targets",
            "Boot process and rescue mode", "Processes and tuned", "journald and logs", "Partitions and fdisk",
            "LVM", "XFS ext4 and fstab", "NFS and autofs", "Swap", "dnf rpm and repositories",
            "cron at and systemd timers", "NetworkManager and nmcli", "Hostname and name resolution",
            "Users groups and sudo", "File permissions ACLs and SGID", "SELinux contexts and booleans",
            "firewalld", "SSH key authentication", "Containers with podman",
        ],
    },
    "aws_saa": {
        "name": "AWS Solutions Architect Associate",
        "description": "AWS SAA-C03: secure, resilient, high-performing and cost-optimized architectures.",
        "objectives": [
            "IAM and policies", "KMS and encryption", "VPC subnets NAT and endpoints",
            "Security groups vs NACLs", "S3 storage classes and lifecycle", "EBS EFS and FSx",
            "RDS and Aurora Multi-AZ and replicas", "DynamoDB", "ELB and Auto Scaling", "Route 53 routing policies",
            "CloudFront", "SQS SNS and EventBridge", "Lambda and serverless", "Disaster recovery strategies",
            "Cost: Savings Plans Spot and right-sizing", "CloudWatch and CloudTrail",
        ],
    },
    "terraform": {
        "name": "Terraform Associate",
        "description": "HashiCorp Terraform Associate: IaC concepts, CLI workflow, state, modules, HCP Terraform.",
        "objectives": [
            "IaC concepts", "Providers and versions", "Resources and data sources", "Variables outputs and locals",
            "Expressions and functions", "Core workflow: init plan apply destroy", "State and backends",
            "State locking and drift", "Modules", "Workspaces", "Import and moved blocks",
            "Sensitive values and secrets", "HCP Terraform and Sentinel",
        ],
    },
}
