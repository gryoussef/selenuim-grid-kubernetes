#!/usr/bin/env python3
import subprocess
import time
import sys
import argparse
import logging
from typing import Tuple

class SeleniumGridDeployer:
    def __init__(self, namespace: str = 'selenium', release_name: str = 'selenium-grid', chart_path: str = './helm'):
        self.namespace = namespace
        self.release_name = release_name
        self.chart_path = chart_path
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def run_command(self, command: list) -> Tuple[bool, str]:
        """Execute a shell command and return its output."""
        try:
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, f"Command failed: {e.stderr}"

    def validate_helm_chart(self) -> bool:
        """Validate the Helm chart."""
        self.logger.info("Validating Helm chart...")
        success, output = self.run_command(['helm', 'lint', self.chart_path])
        if not success:
            self.logger.error(f"Helm chart validation failed: {output}")
        return success

    def deploy(self, node_count: int, max_retries: int) -> bool:
        """Deploy the Helm chart with specified parameters."""
        command = [
            'helm', 'upgrade', '--install',
            self.release_name,
            self.chart_path,
            '--namespace', self.namespace,
            '--create-namespace',
            '--set', f'chromeNode.replicas={node_count}',
            '--set', f'testController.backoffLimit={max_retries}'
        ]

        self.logger.info(f"Deploying Selenium Grid with {node_count} nodes and {max_retries} max retries")
        success, output = self.run_command(command)
        
        if not success:
            self.logger.error(f"Deployment failed: {output}")
        return success

    def wait_for_grid_ready(self, timeout: int = 300) -> bool:
        """Wait for all grid components to be ready."""
        self.logger.info("Waiting for Selenium Grid to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Check pod status
            success, output = self.run_command([
                'kubectl', 'get', 'pods',
                '-n', self.namespace,
                '-o', 'jsonpath={.items[*].status.phase}'
            ])
            
            if not success:
                self.logger.error(f"Failed to get pod status: {output}")
                return False

            phases = output.split()
            if not phases:
                time.sleep(5)
                continue

            # Consider success if all pods are either Running or Succeeded (for jobs)
            if all(phase in ['Running', 'Succeeded'] for phase in phases):
                # Additional check for hub readiness
                success, _ = self.run_command([
                    'kubectl', 'exec', '-n', self.namespace,
                    f'deployment/{self.release_name}-selenium-hub',
                    '--', 'curl', '-s', 'http://localhost:4444/wd/hub/status'
                ])
                
                if success:
                    self.logger.info("Selenium Grid is ready")
                    return True

            time.sleep(5)

        self.logger.error(f"Timeout waiting for Selenium Grid to be ready")
        return False

    def check_deployment_status(self) -> bool:
        """Check the final deployment status."""
        success, output = self.run_command([
            'helm', 'status',
            self.release_name,
            '-n', self.namespace
        ])
        
        if success:
            self.logger.info("Deployment status check successful")
        else:
            self.logger.error(f"Deployment status check failed: {output}")
        return success

def main():
    parser = argparse.ArgumentParser(description='Deploy Selenium Grid')
    parser.add_argument('--node-count', type=int, default=1, help='Number of Chrome nodes')
    parser.add_argument('--max-retries', type=int, default=3, help='Maximum test retries')
    args = parser.parse_args()

    deployer = SeleniumGridDeployer()

    # Validate chart
    if not deployer.validate_helm_chart():
        sys.exit(1)

    # Deploy with specified parameters
    if not deployer.deploy(args.node_count, args.max_retries):
        sys.exit(1)

    # Wait for grid to be ready
    if not deployer.wait_for_grid_ready():
        sys.exit(1)

    # Final status check
    if not deployer.check_deployment_status():
        sys.exit(1)

    deployer.logger.info("Selenium Grid deployment completed successfully")

if __name__ == "__main__":
    main()