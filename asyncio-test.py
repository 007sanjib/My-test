

import asyncio  
import aiohttp  


# using time module
import time
 
# ts stores the time in seconds
# ts = time.time()
 
  
async def fetch(url : str, 
                session : aiohttp.ClientSession,
                json_body : dict  ):  
    
    try:
        async with session.request(method= "POST",
                                url= url,
                                json = json_body) as response:  
            return await response.text()  
    except Exception as ex:
        print("Exception occured while calling the URL ",url, ex)

    
async def main():  
    urls = [  
        'https://conversional-ai-deve.apps.gp-1-nonprod.openshift.cignacloud.com/medicaremultipleplan', 
        'https://conversional-ai-deve.apps.gp-1-nonprod.openshift.cignacloud.com/wrong',  
        'https://conversional-ai-deve.apps.gp-1-nonprod.openshift.cignacloud.com/medicaremultipleplan'
    ] 

    body_list =  \
    [   '{ "query_text": "What is the copayment for inpatient hospital stay?", "folderpath": "2023/Texas/H4513-060-005 Cigna TotalCare HMO D-SNP"}',
        '{ "query_text": "What is the copayment for inpatient hospital stay?", "folderpath": "2023/Texas/H4513-061-001 Cigna Preferred Medicare HMO"}',
        '{ "query_text": "What is the copayment for inpatient hospital stay?", "folderpath": "2023/Texas/H4513-009-000 Cigna Courage Medicare HMO" }'
    ]
  
    async with aiohttp.ClientSession() as session:  
        tasks = []  
        count = 0
        for url in urls:  
            print("Task number = ", count)
            print('URL=', url, 'body=', body_list[count])
            tasks.append(asyncio.ensure_future(fetch(url=url, 
                                                     session=session,
                                                     json_body=eval( body_list[count]) )))  
            count = count + 1

        t1 = time.time()    
        print("START TIME", t1)
        try:
            responses = await asyncio.gather(*tasks)  
        except Exception as ex:
            print("Exception in calling threads", ex)
            
        t2 = time.time()    
        print("END TIME ", t2, " Difference = ", t2-t1)
        for response in responses:  
            print("PRINTING FINAL RESPONSES: ", response)  
            try:
                print(eval(response)["result_text"])
            except Exception as ex:
                # print(response)
                print("API response has a problem.")    
  
if __name__ == '__main__':  
    loop = asyncio.get_event_loop()  
    loop.run_until_complete(main())  
    loop.close()  

