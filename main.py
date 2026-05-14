from imagine import Imagine

if __name__ == '__main__':
    image = Imagine()
    prompts = [
        "uni soviet flag",
        "partai komunis indonesia flag",
    ]
    
    for prompt in prompts:
        response = image.generate(prompt)
        if response:
            print(response)
        
    print("[+] All of process have been played.")
