import os
import asyncio
import json

from pyppeteer import launch


async def init(page):
    await page.evaluate('''
        (function() {
            window.dispatchEvent(new CustomEvent('set-global-style', {
                bubbles: true,
                detail: {
                    data: {"color":{"brand":"#121212","highlight":"#4D4D4D","text-1":"#4D4D4D","text-2":"#121212","text-3":"#FFFFFF","bg-1":"#E2E2E2","bg-2":"#F3F3F3","bg-3":"#FFFFFF","line-1":"#ECECEC","line-2":"#7D7D7D","line-3":"#121212","success":"#428445","error":"#EA3335","warning":"#F2A73B","info":"#1890FF","my-colors":["#121212","#4f4f4f","#e2e2e2","#ffffff","#334fb4","#575757"],"color-index-change":5,"theme-colors":["#121212","#4f4f4f","#e2e2e2","#ffffff","#334fb4","#575757"]},"typography":{"heading-1":{"desktop":{"fontSize":"46px","fontWeight":"400","lineHeight":"130%","fontFamily":"heading"},"tablet":{"fontSize":"46px","fontFamily":"heading","fontWeight":"400"},"mobile":{"fontSize":"41px","fontFamily":"heading","fontWeight":"400"}},"heading-2":{"desktop":{"fontSize":"41px","fontWeight":"400","lineHeight":"130%","fontFamily":"heading"},"tablet":{"fontSize":"41px"},"mobile":{"fontSize":"36px"}},"heading-3":{"desktop":{"fontSize":"52px","fontWeight":"400","lineHeight":"130%","fontFamily":"heading"},"tablet":{"fontSize":"52px","fontFamily":"heading","fontWeight":"400"},"mobile":{"fontSize":"46px","fontFamily":"heading","fontWeight":"400"}},"subheading-1":{"desktop":{"fontSize":"25px","fontWeight":"400","lineHeight":"130%","fontFamily":"heading"},"tablet":{"fontSize":"25px"},"mobile":{"fontSize":"23px"}},"subheading-2":{"desktop":{"fontSize":"18px","fontWeight":"400","lineHeight":"130%","fontFamily":"heading"},"tablet":{"fontSize":"18px"},"mobile":{"fontSize":"16px"}},"subheading-3":{"desktop":{"fontSize":"32px","fontWeight":"400","lineHeight":"130%","fontFamily":"heading"},"tablet":{"fontSize":"32px"},"mobile":{"fontSize":"29px"}},"paragraph-1":{"desktop":{"fontSize":"16px","lineHeight":"180%","fontWeight":"400","fontFamily":"body"},"tablet":{"fontSize":"16px","lineHeight":"180%"},"mobile":{"fontSize":"14px"}},"paragraph-2":{"desktop":{"fontSize":"14px","fontWeight":"400","lineHeight":"180%","fontFamily":"body"},"tablet":{"fontSize":"14px"},"mobile":{"fontSize":"12px"}},"paragraph-3":{"desktop":{"fontSize":"10px","fontWeight":"400","lineHeight":"180%","fontFamily":"body"},"tablet":{"fontSize":"10px"},"mobile":{"fontSize":"9px"}}},"spacing":{"xxs":{"desktop":"2px"},"xs":{"desktop":"4px"},"s":{"desktop":"8px"},"m":{"desktop":"12px"},"l":{"desktop":"16px"},"xl":{"desktop":"24px"},"2xl":{"desktop":"32px"},"3xl":{"desktop":"48px"},"4xl":{"desktop":"80px"},"5xl":{"desktop":"112px"}},"radius":{"small":"3px","medium":"6px","large":"16px"},"font":{"body":{"family":"sans-serif","variants":["200","300","regular","500","600","700","800"],"subsets":["hebrew","latin","latin-ext"],"type":"custom"},"heading":{"family":"sans-serif","variants":["200","300","regular","500","600","700","800"],"subsets":["hebrew","latin","latin-ext"],"type":"custom"},"code":{"family":"sans-serif","variants":["200","300","regular","500","600","700","800"],"subsets":["hebrew","latin","latin-ext"],"type":"custom"}},"container":{"width":{"desktop":"1200px","tablet":"100%","mobile":"100%"},"padding":{"desktop":"16px","tablet":"16px","mobile":"16px"}}},
                },
            }));
        })();
    ''')

async def trigger_init_builder_event(page, data=[]):
    await page.evaluate(f'''
        (function() {{
            window.dispatchEvent(new CustomEvent('init-builder', {{
                bubbles: true,
                detail: {{
                    data: {data},
                }},
            }}));
        }})();
    ''')

async def run(output_codegen, save_codegen_path):
    browser = await launch(
        defaultViewport={
            'width': 1440,
            'height':900
        }
    )
    page = await browser.newPage()
    
    await page.goto('https://builder.gempages.net/builder?shopToken=cGF1bC1uZy1maXguZ2VtcGFnZXMubGl2ZS1mNGJmYjViYS01NmM1LTQyMDQtOTRkYS0zNjdmZmI1ZWQxOTAtMTcyNDM5MzYzNw&storefrontHandle=paul-ng-fix&moneyFormat=${{amount}}&moneyWithCurrencyFormat=${{amount}}%20USD&pageType=GP_STATIC&editorImageToLayout=true&isThemeSectionEditor=false&isOriginTemplate=false')
    await init(page)
    await trigger_init_builder_event(page, output_codegen)
    await asyncio.sleep(5)

    section = await page.querySelector('.ROOT')
    await section.screenshot({'path': save_codegen_path})

    await browser.close()

def capture(output_codegen, save_codegen_path):
    asyncio.get_event_loop().run_until_complete(run(output_codegen, save_codegen_path))
