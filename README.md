
<br />
<div align="center">
  <a href="https://github.com/dottdottdott/trads">
    <img src="https://raw.githubusercontent.com/dottdottdott/trads/main/_logo/solid-logo-orange.svg" alt="TrADS" height="80">
  </a>
  <h2>TrADS</h2>
  <p>
    Trust-Aware Decentralized Social network
    <!--<br />
    <a href="https://vsr.informatik.tu-chemnitz.de/projects/2024/trads/">View Demo</a>
    ·
    <a href="mailto:dirk.leichsenring@informatik.tu-chemnitz.de?subject=Issue on TrADS">Report Bug</a>
    ·
    <a href="mailto:dirk.leichsenring@informatik.tu-chemnitz.de?subject=Question on TrADS">Ask Question</a>
  </p>
</div>

<details open="open">
<summary>Table of Contents</summary>

- [About](#-about)
  - [Built With](#-built-with)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Links To Know](#-links-to-know)

</details>


## 💡 About

TrADS is a prototyp implementation of a [Solid][solid] based decentralized social network utilizing 
a trust awareness component. 


### 🧱 Built With

1. Python 3.11
2. Django v5
3. Python pipenv
4. [Solid File Python][solidfilepython]
5. [Picnic CSS][picniccss]


## ⚡ Getting Started

In order to use TrADS you need a Solid pod. You can use a [Pod Provider][pods] or run [host your own Pod][podservers]. 

1. Clone Git Repository  

2. Setup pipenv in project root:
    ```shell
    pipenv install
    ```
        
3. Modify your Django configuration file ``dssd/settings.py``:  
`SOLID_SETTINGS` contains all the information needed to access you solid pod.  
`PGP_PKEY` should contain a private PGP Key, used to sign messages. The corresponding public key should be linked in your solid profile.  

4. Optional: Setup automated cache update to query solid pods periodically for new content using [Django Q][djangoq]:  
    Open a Django shell using ``python manage.py shell`` and create a Schedule object by running:  
    ```python
    from django_q.models import Schedule
    Schedule.objects.create(
      func='solidsocial.solidclient.socail.update_cache',
      minutes=20,
      repeats=-1
    )
    ```  
    The *minutes* value determines the frequency of the cache update and can be changed appropriately.  
     
## 👟 Usage

1. Run TrADS using Django Development Server
    ```shell
    python manage.py runserver
    ```
2. Optional: If automated cache update was set up it's also necessary to start a Django Q Cluster  
   ```shell
   python manage.py qcluster
   ```

## 📚 Links To Know

[TrADS Demo][tradsdemo]

<!-- Identifiers, in alphabetical order -->
[djangoq]: https://github.com/Koed00/django-q
[nss]: https://github.com/nodeSolidServer/node-solid-server
[picniccss]: https://picnicss.com/
[pods]: https://solidproject.org/users/get-a-pod
[podservers]: https://solidproject.org/for-developers/pod-server
[solid]: https://solidproject.org/
[solidpythonfile]: https://github.com/twonote/solid-file-python
[tradsdemo]: https://vsr.informatik.tu-chemnitz.de/projects/2024/trads/
