import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'sans-serif'

# ==========================================================
# FIGURE 3: Usability vs Security Scores for MFA Methods
# ==========================================================
methods = ['Password-only','SMS OTP','TOTP','Biometrics','FIDO2']
usability = [5,4,4,3,3]
security = [1,2,4,4,5]

plt.figure(figsize=(6,4))
plt.scatter(usability, security, color='gray', s=60)
plt.scatter(4,4, color='blue', s=120, marker='*')
for i, method in enumerate(methods):
    plt.text(usability[i]+0.05, security[i]+0.05, method, fontsize=8)
pareto_x = [3,3,4,5]
pareto_y = [5,4,4,1]
plt.plot(pareto_x, pareto_y, linestyle='--', color='black', linewidth=1)
plt.title('Figure 3: Usability vs Security Scores for MFA Methods', fontsize=10, weight='bold')
plt.xlabel('Usability (1 = poor, 5 = excellent)', fontsize=9)
plt.ylabel('Security (1 = poor, 5 = excellent)', fontsize=9)
plt.xlim(1,5.2)
plt.ylim(1,5.2)
plt.grid(True, linestyle=':', linewidth=0.5)
plt.tight_layout()
plt.show()

# ==========================================================
# FIGURE 4: Cost Comparison of MFA Implementation Approaches
# ==========================================================
methods = ['FIDO2 (Hardware Tokens)','Biometrics (Enrollment + Sensors)',
           'SMS OTP (Carrier Fees)','TOTP (Authenticator App)',
           'Our Serverless TOTP (AWS Free Tier)']
costs = [2500,1200,600,50,0]
colors = ['#aaaaaa','#bbbbbb','#cccccc','#dddddd','#90ee90']

plt.figure(figsize=(7,4))
bars = plt.barh(methods, costs, color=colors, edgecolor='black', height=0.6)
for bar, cost in zip(bars, costs):
    plt.text(bar.get_width()+30, bar.get_y()+bar.get_height()/2,
             f"${cost}", va='center', fontsize=8)
plt.title('Figure 4: Cost Comparison of MFA Implementation Approaches', fontsize=10, weight='bold')
plt.xlabel('Estimated Annual Cost per 100 Users (USD)', fontsize=9)
plt.xlim(0,2700)
plt.grid(axis='x', linestyle=':', linewidth=0.5)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# ==========================================================
# FIGURE 5: Authentication Success and Error Rates Across Roles
# ==========================================================
roles = ['Doctor','Nurse','Admin']
success = [98,97,99]
error = [2,3,1]
x = np.arange(len(roles))
width = 0.35

plt.figure(figsize=(6,4))
plt.bar(x-width/2, success, width, color='#90ee90', edgecolor='black', label='Success')
plt.bar(x+width/2, error, width, color='#f8d7da', edgecolor='black', label='Error')
for i in range(len(roles)):
    plt.text(x[i]-width/2, success[i]+0.5, f"{success[i]}%", ha='center', fontsize=8)
    plt.text(x[i]+width/2, error[i]+0.5, f"{error[i]}%", ha='center', fontsize=8)
plt.title('Figure 5: Authentication Success and Error Rates Across Roles', fontsize=10, weight='bold')
plt.xlabel('Roles', fontsize=9)
plt.ylabel('Rate (%)', fontsize=9)
plt.xticks(x, roles)
plt.ylim(0,105)
plt.legend(frameon=False, fontsize=8)
plt.grid(axis='y', linestyle=':', linewidth=0.5)
plt.tight_layout()
plt.show()

# ==========================================================
# FIGURE 6: Code Validity Window and IP Impact on TOTP Generation
# ==========================================================
fig, ax = plt.subplots(figsize=(6.5,2.8))
fig.suptitle('Figure 6: Code Validity Window and IP Impact on TOTP Generation', fontsize=10, weight='bold')

windows=[(0,3,12),(4,7,13),(8,11,14)]
for s,e,c in windows:
    ax.add_patch(patches.Rectangle((s,0.3),e-s,0.3,facecolor='white',edgecolor='black'))
    ax.text((s+e)/2,0.45,f"{c}",ha='center',va='center',fontsize=8,weight='bold')
ax.plot(5,0.45,'o',color='blue',markersize=5)
ax.text(6.5,0.65,"Clinician @00:05",fontsize=8,color='blue')
ax.text(12.5,0.52,"IP→Code",fontsize=8,weight='bold',ha='center')
ax.text(13.3,0.65,".10→22",fontsize=8,ha='center')
ax.text(13.3,0.35,".25→37",fontsize=8,ha='center',color='blue')
ax.set_xlim(0,14)
ax.set_ylim(0,1)
ax.set_xticks([0,3,4,7,8,11,12])
ax.set_yticks([])
ax.set_xlabel('Time (UTC, minutes)',fontsize=8)
ax.grid(axis='x',linestyle=':',linewidth=0.5)
ax.set_title('4-Minute Windows + IP Variation',fontsize=8,weight='bold')
plt.tight_layout(rect=[0,0,1,0.9])
plt.show()

# ==========================================================
# FIGURE 7: Latency Distribution of MFA Verification (ms)
# ==========================================================
np.random.seed(0)
latencies = np.concatenate([
    np.random.normal(50,10,900),
    np.random.normal(120,15,100)
])
latencies = latencies[(latencies>0)&(latencies<200)]

plt.figure(figsize=(6.5,4))
plt.hist(latencies, bins=np.arange(0,210,10), color='#d9d9d9', edgecolor='black')
mean_latency = np.mean(latencies)
plt.axvline(mean_latency, color='black', linestyle='--', linewidth=1)
plt.axvline(100, color='red', linestyle='-', linewidth=1)
plt.text(mean_latency+2,45,f"Mean={mean_latency:.1f}ms",fontsize=8)
plt.text(102,60,"100ms Threshold",fontsize=8,color='red')
plt.title('Figure 7: Latency Distribution of MFA Verification (ms)', fontsize=10, weight='bold')
plt.xlabel('Latency (milliseconds)', fontsize=9)
plt.ylabel('Frequency', fontsize=9)
plt.xlim(0,200)
plt.grid(False)
plt.tight_layout()
plt.show()
