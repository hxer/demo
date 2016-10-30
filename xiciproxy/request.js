var page = require('webpage').create(),
    system = require('system'),
    address;

if (system.args.length === 1){
    console.log('[!Error] Usage: ' + system.args[0] + " <URL>");
    phantom.exit(1);
} else {
    address = system.args[1];

    // settings
    page.settings.resourceTimeout = 60000; // 60s
    page.settings.XSSAuditingEnable = true;
    page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';
    page.customHeaders = {
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    };
    
    page.open(address, function(status) {
        if (status !== 'success') {
            console.log('[!Failed] fail to load the address');
        } else {
            console.log(page.content);
        }
        phantom.exit(0)
    });
}