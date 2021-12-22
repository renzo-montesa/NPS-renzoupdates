docker stop npflaskapp

docker build . -t npflaskapp

docker run -d `
  --name npflaskapp `
  --rm -it -p 5000:5000/tcp `
  --network newpayroll `
  -v "C:/Users/LENOVO-PC/Desktop/NEW PAYROLL PROJECT/Python/new-payroll-v2/reports:/app/reports" `
  -v "C:/Users/LENOVO-PC/Desktop/NEW PAYROLL PROJECT/Python/new-payroll-v2/uploads:/app/uploads" `
  npflaskapp

Write-Host "npflaskapp successfully restarted"