# Todo-en-uno

Paso a paso

Instalar Docker y mysql workbench

docker --version

pip install pymysql

pip install Flask-SQLAlchemy



1. Configurar e iniciar el contenedor de MySQL en Docker
Luego de instalar docker asegurarse de que pulleaste los ultimos datos del github

 1.1 Creacion Container

     docker-compose up -d
      
    docker ps
    
    Estos comandos te permiten crear y ver el container en tu computador
 1.2 Conexion con MySQL Workbench
    Una vez montado el container e instalado el mysql workbench entra y crea una nueva conexion
    Al ingresar los datos usa los siguientesz

    Hostname 127.0.0.1 (Direccion IP default)
    Port 3306 (Puerto default)
    Username myuser
    Password mypassword
    Testeas la conexion y listo
2. Montar BD 
    Despues de tener todo listo en la terminal del proyecto ejecutas

    docker exec -i SQLSERVER mysql -u myuser -pmypassword mydatabase < backup.sql(El archivo estara en el git del proyecto)

    y ya tienes la BD conectada

    Comando para exportar datos de la BD que hiciste o actualizaste
    
    docker exec SQLSERVER mysqldump -u myuser -pmypassword mydatabase > backup.sql

    si no los deja editar cosas por cosas de privilegios usan los siguientes comandos


    docker exec -it my_mysql_db mysql -u root -p
    
    rootpassword 
    
    GRANT PROCESS, RELOAD, LOCK TABLES ON *.* TO 'myuser'@'%';
    FLUSH PRIVILEGES;
    
    docker exec my_mysql_db mysqldump -u myuser -pmypassword mydatabase > backup.sql



