from moov.__init__ import app as application
import glob
import subprocess

# Chemin vers le dossier des templates
templates_path = 'moov/templates/*.html'  # Assurez-vous que le chemin correspond à l'emplacement de vos templates
template_files = glob.glob(templates_path, recursive=True)  # Utilisez recursive=True si vous avez des sous-dossiers

css_files = glob.glob('moov/assets/styles/*.css', recursive=True)
js_files = glob.glob('moov/assets/scripts/*.js', recursive=True)

def reload_install():
    try:
        # Exécute la commande dans le shell
        subprocess.check_call(['pip', 'install', '.', '--no-deps' , '--ignore-installed'])
        print("Le paquet a été installé avec succès sans dépendances.")
    except subprocess.CalledProcessError as e:
        print("Une erreur s'est produite lors de l'installation du paquet.")

if __name__ == "__main__":
    reload_install()

    print("############# " )
    application.run(host="0.0.0.0", port=8080, debug=True, threaded=True , extra_files=template_files + css_files + js_files)