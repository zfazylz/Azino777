import random

from django.http import JsonResponse
from django.shortcuts import render, redirect

from customUser.models import CustomUser, Transactions
from game.models import BetRoll

isWin = True
xValue = 1


def checkCombination(dices):
    combination = 'Straight'
    dices = sorted(dices)
    global xValue
    global isWin

    for i in range(4):
        if not dices[i + 1] - dices[i] == 1:
            combination = 'None'
            isWin = False
            xValue = 7776 / 14
            break

    counter = []
    for dice in list(set(dices)):
        counter.append(dices.count(dice))

    pairs = counter.count(2)
    set3 = counter.count(3)
    four = counter.count(4)
    five = counter.count(4)
    total = 1200
    if pairs == 1:
        combination = 'Pair'
        isWin = True
        xValue = total / 3600
    if pairs == 2:
        combination = 'Pairs'
        xValue = total / 1800
        isWin = True
    if set3 == 1:
        combination = 'Set'
        isWin = True
        xValue = total / 1200
    if pairs == 1 and set == 1:
        combination = 'Ful House'
        xValue = total / 300
        isWin = True
    if four == 1:
        combination = 'Four of Kinds'
        isWin = True
        xValue = total / 150
    if five == 1:
        combination = 'It`s right time to go Kapchigai'
        xValue = total / 6
        isWin = True
    # xValue *= 100/108
    return combination


def gamePageView(request):
    global winCombo, isWin
    userObj = request.user
    userBalance = request.user.balance
    sendValues = {'dices': ['-', '-', '-', '-', '-'],
                  'userBalance': userBalance,
                  'username': userObj.username,
                  'is_valid': False,
                  }
    if BetRoll.objects.filter(user=userObj).count() > 0:
        bets = BetRoll.objects.filter(user=userObj).order_by('id')[::-1][:10]
        sendValues['userBets'] = [[bet.combination, bet.betValue, bet.winLoseValue] for bet in bets]

    if request.is_ajax():
        # userBalance = 1000000
        betValue = request.POST.get('betValue')
        if not betValue:
            betValue = 0
        elif not isinstance(betValue, int):
            betValue = int(betValue)
        userBalance -= betValue
        if userBalance < 0:
            return render(request, 'lowBalance.html', sendValues)

        sendValues['is_valid'] = True
        dices = [random.randint(1, 6),
                 random.randint(1, 6),
                 random.randint(1, 6),
                 random.randint(1, 6),
                 random.randint(1, 6)]
        sendValues['dices'] = dices
        combination = checkCombination(dices)
        sendValues['combination'] = combination
        winLooseValue = -betValue
        if isWin:
            winLooseValue = int(betValue * xValue)
            userBalance += winLooseValue
        sendValues['userBalance'] = userBalance

        BetRoll.objects.create(user=userObj,
                               betValue=betValue,
                               winLoseValue=winLooseValue,
                               combination=str(dices[0]) + str(dices[1]) + str(dices[2]) + str(dices[3]) + str(dices[4])
                               )

        if BetRoll.objects.filter(user=userObj).count():
            bets = BetRoll.objects.filter(user=userObj).order_by('id')[::-1][:10]
            sendValues['userBets'] = [[bet.combination, bet.betValue, bet.winLoseValue] for bet in bets]

        CustomUser.objects.select_for_update().filter(id=userObj.id).update(balance=userBalance)
        return JsonResponse(sendValues)
    return render(request, 'game.html', sendValues)


def homePageView(request):
    return render(request, 'index.html')


def fillCashView(request):
    if request.POST.get('pay') == 'Pay':
        amount = int(request.POST.get('fillBalance'))
        userBalance = request.user.balance
        Transactions.objects.create(user=request.user, amount=amount)
        CustomUser.objects.select_for_update().filter(id=request.user.id).update(balance=userBalance + amount)
        return redirect('game')

    return render(request, 'lowBalance.html', {})


def withdrawCashView(request):
    if request.POST.get('Withdraw') == 'Withdraw':
        amount = int(request.POST.get('withdrawBalance'))
        userBalance = request.user.balance
        Transactions.objects.create(user=request.user, amount=amount * -1)
        CustomUser.objects.select_for_update().filter(id=request.user.id).update(balance=userBalance - amount)
        return redirect('game')

    return render(request, 'withdrawBalance.html', {})
