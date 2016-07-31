const http = require('http');
const req = http.get('http://www.baidu.com', (res) => {
    console.log(res.statusCode);
});
