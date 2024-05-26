addEventListener('fetch', event => {
	event.respondWith(handleRequest(event.request));
  });
  
  async function handleRequest(request) {
	const url = new URL(request.url);
	const targetUrl = new URL('https://mc.999.com.cn' + url.pathname + url.search); 
  
	// 创建新 Headers 对象，排除以 'cf-' 开头的请求头
	let newHeaders = new Headers();
	for (let pair of request.headers.entries()) {
	  if (!pair[0].startsWith('cf-')) {
		newHeaders.append(pair[0], pair[1]);
	  }
	}
  
	// 创建一个新的请求以访问目标 URL
	const modifiedRequest = new Request(targetUrl, {
	  headers: newHeaders,
	  method: request.method,
	  body: request.body,
	  redirect: 'manual'
	});
  
	try {
	  const response = await fetch(modifiedRequest);
	  let modifiedResponse;
  
	  // 处理重定向
	  if ([301, 302, 303, 307, 308].includes(response.status)) {
		const location = new URL(response.headers.get('location'));
		modifiedResponse = new Response(null, {
		  status: response.status,
		  statusText: response.statusText,
		  headers: {
			'Location': location.href
		  }
		});
	  } else {
		modifiedResponse = new Response(response.body, {
		  status: response.status,
		  statusText: response.statusText,
		  headers: response.headers
		});
	  }
  
	  // 添加 CORS 头部，允许跨域访问
	  modifiedResponse.headers.set('Access-Control-Allow-Origin', '*');
	  modifiedResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
	  modifiedResponse.headers.set('Access-Control-Allow-Headers', '*');
  
	  return modifiedResponse;
	} catch (error) {
	  return new Response('无法访问目标地址: ' + error.message, {
		status: 500
	  });
	}
  }
