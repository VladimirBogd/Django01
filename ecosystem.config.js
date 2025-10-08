module.exports = {
  apps: [
    {
      name: 'django',
      script: 'C:\\Users\\vovab\\AppData\\Local\\Programs\\Python\\Python312\\python.exe',
      args: 'manage.py runserver 127.0.0.1:8000',
      cwd: 'C:\\Users\\vovab\\Desktop\\Флешка\\4 курс (1 семестр)\\Основы DevOps\\DevOps_LAB1\\Django01_server',
      interpreter: 'none'
    },
    {
      name: "vue",
      cwd: "C:\\Users\\vovab\\Desktop\\Флешка\\4 курс (1 семестр)\\Основы DevOps\\DevOps_LAB1\\Django01_server\\client",
      script: "cmd",
      args: "/c npm run dev",
      interpreter: "none"
    }
  ]
};