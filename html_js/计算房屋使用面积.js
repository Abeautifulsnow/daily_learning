// 使用方式: 可以直接将代码copy到浏览器控制窗口去运行.

(function () {
  // 计算实际使用面积
  var sum = 0;
  var d = document.getElementById('infoList').getElementsByClassName('row')
  var rows = []
  for (var i in d) (
    rows.push(d[i])
  )
  rows.map(v => {
    if (typeof v == 'object') {
      sum += (v.getElementsByClassName('col')[1].innerText.replace('平米', '') - 0)
    }
  })

  // 获取标注面积
  var vituralS = document.getElementsByClassName('mainInfo')[2].innerText.replace('平米', '') - 0

  var C = document.createElement('div')
  C.classList.add('area')
  var C1 = document.createElement('div')
  C1.classList.add('mainInfo')
  C1.innerText = `${Math.round(sum)} (${sum}) ㎡`
  C1.style.color = 'red'
  C1.style.fontSize = '15px'
  var C2 = document.createElement('div')
  C2.classList.add('subInfo')
  C2.innerText = `实际使用面积`
  C2.style.color = 'red'
  C.append(C1)
  C.append(C2)
  var CC = document.createElement('div')
  CC.classList.add('area')
  var C3 = document.createElement('div')
  C3.classList.add('mainInfo')
  C3.innerText = `${Math.round(sum / vituralS * 100)}%`
  C3.style.color = 'red'
  var C4 = document.createElement('div')
  C4.classList.add('subInfo')
  C4.innerText = `得房率`
  C4.style.color = 'red'
  CC.append(C3)
  CC.append(C4)
  C.style.marginTop = '20px'
  C.style.marginRight = '5px'
  C.style.borderRight = '1px solid darkgrey'
  CC.style.marginTop = '20px'
  document.getElementsByClassName('houseInfo')[0].append(C)
  document.getElementsByClassName('houseInfo')[0].append(CC)
  // Your code here...
})();