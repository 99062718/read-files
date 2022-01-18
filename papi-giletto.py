import tkinter
from tkinter import ttk, StringVar, IntVar, messagebox

mainWindow = tkinter.Tk()
mainWindow.configure(padx=50, pady=10)

content = []
amountBolletjes = 0
hoorntjes = 0
bakjes = 0
extras = {
    "smaakjes":{
        "Aardbei": 0,
        "Chocolade": 0,
        "Vanille": 0
    },
    "toppings":{
        "Geen": 0,
        "Slagroom": 0,
        "Sprinkels": 0,
        "Caramel saus": 0
    }
}
prices = {
    "bolletje": 0.95,
    "hoorntje": 1.25,
    "bakje": 0.75,
    "toppings":{
        "Geen": 0,
        "Slagroom": 0.5,
        "Sprinkels": 0.3
    }
}
toppingCosts = 0

textLabel = tkinter.Label()
textLabel.grid(column=0, row=0)

contentBox = tkinter.Frame()
contentBox.grid(column=0, row=1)

submitBtn = tkinter.Button(text="Start")
submitBtn.grid(column=0, row=2)

def contentCreator(labelText, toCreate="", extraValues=[]):
    global answer
    textLabel.configure(text=labelText)

    if toCreate == "radio":
        num = 0
        answer = StringVar(mainWindow, "")
        for value in extraValues:
            content.append(
                ttk.Radiobutton(
                    contentBox,
                    text=value,
                    value=value,
                    variable=answer
                )
            )
            content[num].grid(column=0, row=num)
            num += 1
    elif toCreate == "spinbox":
        answer = IntVar(mainWindow, 1)
        content.append(
            ttk.Spinbox(
                contentBox,
                from_=1,
                to=float("inf"),
                textvariable=answer
            )
        )
        content[0].grid(column=0, row=0)
    else:
        num = 0
        for value in extraValues:
            content.append(
                tkinter.Label(
                    contentBox,
                    text=value
                )
            )
            content[num].grid(column=0, row=num)
            num += 1

def theContentDestroyer9000(moreToDestroy=[]): # Hey, you! Yeah, you! Have you ever felt like the world would be better without all that stupid content? Well i've got just the thing for you. Introducing: theContentDestroyer9000! Now that pesky content cant bother us anymore!
    global content
    for content in (content, moreToDestroy):
        for box in content:
            box.destroy()
    content = []

def beginScreen():
    submitBtn.configure(text="Submit", command=zakelijkOfParticulierQuestion)
    contentCreator("Bent u particulier of zakelijk?", "radio", ["Particulier", "Zakelijk"])

def zakelijkOfParticulierQuestion():
    global zakelijkOfParticulier, aantalToGiveSmaakje, currentBolletje
    currentBolletje = 1
    aantalToGiveSmaakje = []

    if answer.get() != "":
        if answer.get() == "Zakelijk":
            zakelijkOfParticulier = "Zakelijk"
        elif answer.get() == "Particulier":
            zakelijkOfParticulier = "Particulier"

        theContentDestroyer9000()
        submitBtn.configure(command=howManyBolletjes)
        contentCreator("Hoeveel {} wilt u?".format("bolletjes" if zakelijkOfParticulier == "Particulier" else "liters"), "spinbox")
    else:
        messagebox.showerror(message="Sorry dat is geen optie die we aanbieden...")

def howManyBolletjes():
    global amountBolletjes
    aantalToGiveSmaakje.append(answer.get())

    if aantalToGiveSmaakje[0] < 9 or zakelijkOfParticulier == "Zakelijk":
        if currentBolletje <= aantalToGiveSmaakje[0]:
            submitBtn.configure(command=smaakjeValidator)
            theContentDestroyer9000()
            contentCreator("Welke smaak moet {} {} zijn?".format("bolletje" if zakelijkOfParticulier == "Particulier" else "liter", currentBolletje), "radio", list(extras["smaakjes"].keys()))
        else:
            amountBolletjes += aantalToGiveSmaakje[0]
            theContentDestroyer9000()
            if zakelijkOfParticulier == "Particulier":
                if aantalToGiveSmaakje[0] < 4:
                    contentCreator("Wilt u deze {} bolletje(s) in een hoorntje of een bakje?".format(aantalToGiveSmaakje[0]), "radio", ["hoorntje", "bakje"])
                    submitBtn.configure(command=hoorntjeOfBakje)
                elif aantalToGiveSmaakje[0] > 3:
                    prices["toppings"]["Caramel saus"] = 0.9
                    messagebox.showinfo(message="Dan krijgt u van mij een bakje met {} bolletjes".format(aantalToGiveSmaakje[0]))
                    contentCreator("Wat voor toppings wilt u?", "radio", list(extras["toppings"].keys()))
                    submitBtn.configure(command=toppingValidator)
            else:
                prices["bolletje"] = 9.8
                contentCreator("Wilt u nog meer bestellen?", "radio", ["ja", "nee"])
                submitBtn.configure(command=againBestellen)
    else:
        messagebox.showerror(message="Sorry, zulke grote bakken hebben we niet")

def smaakjeValidator():
    global extras, currentBolletje
    falseAnswer = True

    for smaakje in list(extras["smaakjes"].keys()):
        if smaakje == answer.get():
            extras["smaakjes"][smaakje] += 1
            currentBolletje += 1
            falseAnswer = False
            break
    
    if falseAnswer:
        messagebox.showerror(message="Sorry dat is geen optie die we aanbieden...")

    howManyBolletjes()
    
    
def hoorntjeOfBakje():
    global hoorntjes, bakjes

    if answer.get() != "":
        if answer.get() == "hoorntje":
            prices["toppings"]["Caramel saus"] = 0.6
            hoorntjes += 1
        elif answer.get() == "bakje":
            prices["toppings"]["Caramel saus"] = 0.9
            bakjes += 1
        theContentDestroyer9000()
        contentCreator("Wat voor toppings wilt u?", "radio", list(extras["toppings"].keys()))
        submitBtn.configure(command=toppingValidator)
    else:
        messagebox.showerror(message="Sorry dat is geen optie die we aanbieden...")

def toppingValidator():
    global extras, toppingCosts
    falseAnswer = True

    for topping in list(extras["toppings"].keys()):
        if topping == answer.get():
            extras["toppings"][topping] += 1
            falseAnswer = False

            theContentDestroyer9000()
            contentCreator("Wilt u nog meer bestellen?", "radio", ["ja", "nee"])
            submitBtn.configure(command=againBestellen)

            toppingCosts += prices["toppings"][topping]
            break
    
    if falseAnswer:
        messagebox.showerror(message="Sorry dat is geen optie die we aanbieden...")

def againBestellen():
    if answer.get() == "ja":
        theContentDestroyer9000()
        zakelijkOfParticulierQuestion()
    elif answer.get() == "nee":  
        bolletjesCost = amountBolletjes * prices["bolletje"]
        hoorntjesCost = hoorntjes * prices["hoorntje"]
        bakjesCost = bakjes * prices["bakje"]
        totalCost = bolletjesCost + hoorntjesCost + bakjesCost + toppingCosts

        theContentDestroyer9000([submitBtn])          
        contentCreator("Bedankt en tot ziens!", "label", [
            '-----------["Papi gileto"]-----------',
            "{}             {} x €{}     = €{}".format("Bolletje" if zakelijkOfParticulier == "Particulier" else "Liter", amountBolletjes, prices["bolletje"], bolletjesCost),
            "Hoorntje             {} x €{}     = €{}".format(hoorntjes, prices["hoorntje"], hoorntjesCost) if hoorntjesCost > 0 else "",
            "Bakje             {} x €{}     = €{}".format(bakjes, prices["bakje"], bakjesCost) if bakjesCost > 0 else "",
            "Topping                          = €{}".format(toppingCosts) if toppingCosts > 0 else "",
            "                              ------- +",
            "Totaal                      = €{}".format(totalCost),
            "BTW (9%)                    = €{}".format(round(totalCost/106 * 6, 2))
        ])
    else:
        messagebox.showerror(message="Sorry dat is geen optie die we aanbieden...")

contentCreator("Welkom bij Papi Gelato.")
submitBtn.configure(command=beginScreen)

mainWindow.mainloop()