# Manual Test Cases for Threat Attribution

##  Benign URL
**Input Features**: Trusted SSL, no IP address, no prefix/suffix, no political keyword  
**Expected Output**:  
- Classification: BENIGN  
- Attribution: Not applicable

## Malicious – State-Sponsored
**Input Features**: SSLfinal_State=1, Prefix_Suffix=1  
**Expected Output**:  
- Classification: MALICIOUS  
- Attribution: State-Sponsored

## Malicious – Organized Cybercrime
**Input Features**: Shortining_Service=1, having_IP_Address=1  
**Expected Output**:  
- Classification: MALICIOUS  
- Attribution: Organized Cybercrime

## Malicious – Hacktivist
**Input Features**: has_political_keyword=1  
**Expected Output**:  
- Classification: MALICIOUS  
- Attribution: Hacktivist
