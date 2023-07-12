class Upgrade:
    def upgrade(self):
        """"apt-get upgrade"""
        self.deployment_dir = self.ostree.current_deployment()

        self.console.print("Upgrading packages")
        self.apt_upgrade()

        self.ostree.post_deployment()
