import docker
import yaml
import logging
import psycopg2
import time
import sys

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] IRONSTACK_CORE: %(message)s'
)
logger = logging.getLogger(__name__)

class IronstackOrchestrator:
    def __init__(self, config_file="config.yaml"):
        self.client = docker.from_env()
        try:
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
            logger.info("Configuration IRONSTACK chargée avec succès.")
        except FileNotFoundError:
            logger.error("Fichier config.yaml introuvable à la racine.")
            sys.exit(1)

    def verify_container(self, name):
        """Check container lifecycle via Docker-py"""
        try:
            container = self.client.containers.get(name)
            if container.status == 'running':
                logger.info(f"✔ [DOCKER] {name} est opérationnel.")
                return True
            logger.warning(f"✘ [DOCKER] {name} est à l'arrêt (Status: {container.status}).")
            return False
        except docker.errors.NotFound:
            logger.error(f"✘ [DOCKER] {name} n'existe pas. Vérifiez le déploiement.")
            return False

    def verify_postgres_logic(self, db_conf):
        """Deep health-check: Testing real DB handshake"""
        try:
            # On teste sur localhost car le script tourne sur l'hôte
            conn = psycopg2.connect(
                host="localhost", 
                database=db_conf['database'],
                user=db_conf['user'],
                password=db_conf['password'],
                port=db_conf['port']
            )
            conn.close()
            logger.info("✔ [DB] PostgreSQL accepte les connexions SQL.")
            return True
        except Exception as e:
            logger.error(f"✘ [DB] Échec de connexion SQL: {e}")
            return False

    def audit_infrastructure(self):
        """Global scan of IRONSTACK layers"""
        logger.info(f"--- DÉBUT DE L'AUDIT : {self.config['infrastructure_name']} ---")
        success = True

        for svc in self.config['services']:
            # Validation Docker
            if not self.verify_container(svc['name']):
                success = False
            
            # Validation Applicative (Postgres)
            if svc.get('type') == 'database' and success:
                if not self.verify_postgres_logic(svc['db_config']):
                    success = False

        if success:
            logger.info("🚀 RÉSULTAT : Infrastructure validée et prête pour la production.")
        else:
            logger.error("🚨 RÉSULTAT : Échec de l'audit. Vérifiez les logs ci-dessus.")

if __name__ == "__main__":
    orchestrator = IronstackOrchestrator()
    orchestrator.audit_infrastructure()

