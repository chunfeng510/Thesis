from mytool import perl_script
import subprocess
# perl_script.generator('C0040034', 'C0023530')

perl_script.generator('C0040034', 'C0023530')
Command = "run.pl"
perl_process = subprocess.Popen(["perl", Command], stdout = subprocess.PIPE)
for line in iter(perl_process.stdout.readline, b''):
    print(line.rstrip())