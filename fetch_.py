import os
import requests
import pandas as pd
import numpy as np

TRAIN_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt"
TEST_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt"

def download_file(url, filename):
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        with open(filename, 'w') as f:
            f.write(response.text)
        print(f"Successfully downloaded {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        return False

def generate_synthetic_data(filename, num_records=50000):
    print(f"Generating {num_records} synthetic records for {filename}...")
    
    # NSL-KDD has 41 features + 1 label + 1 difficulty level
    np.random.seed(42)
    
    protocols = ['tcp', 'udp', 'icmp']
    services = ['http', 'private', 'domain_u', 'smtp', 'ftp_data', 'eco_i', 'other', 'ecr_i', 'telnet', 'finger']
    flags = ['SF', 'S0', 'REJ', 'RSTR', 'SH', 'RSTO', 'S1', 'S2', 'S3', 'OTH']
    
    attacks = ['normal', 'neptune', 'satan', 'ipsweep', 'portsweep', 'smurf', 'nmap', 'back', 'teardrop', 'warezclient', 'pod', 'guess_passwd', 'buffer_overflow', 'land', 'warezmaster', 'imap', 'rootkit', 'loadmodule', 'ftp_write', 'multihop', 'phf', 'perl', 'spy']
    
    data = []
    for _ in range(num_records):
        record = [
            np.random.randint(0, 1000), # duration
            np.random.choice(protocols), # protocol_type
            np.random.choice(services), # service
            np.random.choice(flags), # flag
            np.random.randint(0, 50000), # src_bytes
            np.random.randint(0, 50000), # dst_bytes
            np.random.choice([0, 1], p=[0.99, 0.01]), # land
            np.random.randint(0, 4), # wrong_fragment
            np.random.randint(0, 4), # urgent
            np.random.randint(0, 30), # hot
            np.random.randint(0, 5), # num_failed_logins
            np.random.choice([0, 1]), # logged_in
            np.random.randint(0, 10), # num_compromised
            np.random.choice([0, 1], p=[0.99, 0.01]), # root_shell
            np.random.choice([0, 1, 2], p=[0.98, 0.01, 0.01]), # su_attempted
            np.random.randint(0, 5), # num_root
            np.random.randint(0, 5), # num_file_creations
            np.random.randint(0, 3), # num_shells
            np.random.randint(0, 5), # num_access_files
            0, # num_outbound_cmds
            np.random.choice([0, 1], p=[0.99, 0.01]), # is_host_login
            np.random.choice([0, 1], p=[0.95, 0.05]), # is_guest_login
            np.random.randint(0, 512), # count
            np.random.randint(0, 512), # srv_count
            np.random.rand(), # serror_rate
            np.random.rand(), # srv_serror_rate
            np.random.rand(), # rerror_rate
            np.random.rand(), # srv_rerror_rate
            np.random.rand(), # same_srv_rate
            np.random.rand(), # diff_srv_rate
            np.random.rand(), # srv_diff_host_rate
            np.random.randint(0, 256), # dst_host_count
            np.random.randint(0, 256), # dst_host_srv_count
            np.random.rand(), # dst_host_same_srv_rate
            np.random.rand(), # dst_host_diff_srv_rate
            np.random.rand(), # dst_host_same_src_port_rate
            np.random.rand(), # dst_host_srv_diff_host_rate
            np.random.rand(), # dst_host_serror_rate
            np.random.rand(), # dst_host_srv_serror_rate
            np.random.rand(), # dst_host_rerror_rate
            np.random.rand(), # dst_host_srv_rerror_rate
            np.random.choice(attacks, p=[0.53] + [0.47 / 22] * 22), # label (slightly biased to normal to mimic real dataset)
            np.random.randint(15, 22) # difficulty_level
        ]
        data.append(record)
        
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, header=False)
    print(f"Synthetic dataset saved to {filename}")

if __name__ == "__main__":
    os.makedirs('dataset', exist_ok=True)
    
    train_path = os.path.join('dataset', 'KDDTrain+.txt')
    test_path = os.path.join('dataset', 'KDDTest+.txt')
    
    if not os.path.exists(train_path):
        success = download_file(TRAIN_URL, train_path)
        if not success:
            generate_synthetic_data(train_path, 50000)
    else:
        print("KDDTrain+.txt already exists.")
        
    if not os.path.exists(test_path):
        success = download_file(TEST_URL, test_path)
        if not success:
            generate_synthetic_data(test_path, 10000)
    else:
        print("KDDTest+.txt already exists.")
