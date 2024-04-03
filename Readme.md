# Usages:
```
cd PointCloud2BinaryImage
python3 CrackAnalyzer.py
```
## Case 0:
http://127.0.0.1:5002/analyze_crack?click1_x=0.08817603&click1_y=0.10874449&click2_x=0.11819754&click2_y=0.14

{
  "total_crack_length": 0
}

## Case 1:
http://127.0.0.1:5002/analyze_crack?click1_x=-10&click1_y=11&click2_x=0&click2_y=20

{
  "total_crack_length": 261.0
}

# Autorun configuration
Certainly! Here are the detailed steps to configure Supervisor to automatically start your Gunicorn server on system boot:

1. Install Supervisor:
   - On Ubuntu or Debian:
     ```
     sudo apt-get install supervisor
     ```
   - On CentOS or RHEL:
     ```
     sudo yum install supervisor
     ```

2. Create a Supervisor configuration file for your API:
   - Create a new file with a `.conf` extension (e.g., `crack_analyzer_api.conf`) in the Supervisor configuration directory (usually `/etc/supervisor/conf.d/`).
   - Open the file in a text editor with sudo privileges, for example:
     ```
     sudo nano /etc/supervisor/conf.d/crack_analyzer_api.conf
     ```

3. Add the following configuration to the file:
   ```
   [program:crack_analyzer_api]
   directory=/path/to/your/api/directory
   command=/path/to/your/virtual/environment/bin/gunicorn --bind 0.0.0.0:5000 crack_analyzer_api:app
   autostart=true
   autorestart=true
   startretries=3
   stderr_logfile=/var/log/crack_analyzer_api.err.log
   stdout_logfile=/var/log/crack_analyzer_api.out.log
   user=your_username
   ```

   Replace the following placeholders:
   - `/path/to/your/api/directory`: The directory where your `crack_analyzer_api.py` file is located.
   - `/path/to/your/virtual/environment/bin/gunicorn`: The path to the Gunicorn executable in your virtual environment.
   - `your_username`: The username under which you want to run the API process.

   Save the file and exit the text editor.

4. Update Supervisor configuration:
   ```
   sudo supervisorctl reread
   sudo supervisorctl update
   ```

   This will make Supervisor aware of the new configuration file.

5. Start your API using Supervisor:
   ```
   sudo supervisorctl start crack_analyzer_api
   ```

   This will start your Gunicorn server and make your API accessible.

6. Configure Supervisor to start on system boot:
   - On Ubuntu or Debian:
     - The Supervisor daemon should already be configured to start on boot by default.
   - On CentOS or RHEL:
     - Open the Supervisor configuration file:
       ```
       sudo nano /etc/supervisord.conf
       ```
     - Uncomment the following line to enable Supervisor to start on boot:
       ```
       [supervisord]
       ...
       autostart=true
       ...
       ```
     - Save the file and exit the text editor.

7. Reboot your system to test the automatic startup:
   ```
   sudo reboot
   ```

   After the reboot, your Gunicorn server should automatically start, and your API should be accessible.

You can check the status of your API process using the following command:
```
sudo supervisorctl status crack_analyzer_api
```

If you encounter any issues or need to manage your API process, you can use Supervisor commands like `start`, `stop`, `restart`, and `status` with `sudo supervisorctl`.

By following these steps, you can configure Supervisor to automatically start your Gunicorn server and your API on system boot, ensuring that your API is always available without manual intervention.