function loadschool(schoolstr,departmentstr)
{
	var datas = {"数学科学学院":["数学与应用数学","信息与计算科学","统计学","其他"],"物理与材料科学学院":["应用物理学","材料物理","光信息科学与技术","信息显示与光电技术","其他"],"化学化工学院":["化学","应用化学","化学工程与工艺","高分子材料与工程","材料化学","新能源材料与器件","其他"],"计算机科学与技术学院":["计算机与技术","软件工程","网络工程","信息安全","其他"],"电子信息工程学院":["电子信息工程","通信工程","微电子学","物联网工程","其他"],"电气工程与自动化学院":["自动化","电气工程及其自动化","测控技术与仪器","机械设计制造及其自动化","其他"],"生命科学学院":["生物科学","生物技术","生物工程","其他"],"资源与环境工程学院":["环境科学","地理信息系统","地质学","其他"],"文学院":["汉语言文学","对外汉语","其他"],"历史系":["历史学","考古学","其他"],"哲学系":["哲学","应用心理学","其他"],"新闻传播学院":["新闻学","编辑出版学","广播电视新闻学","广告学","数字媒体艺术","其他"],"经济学院":["经济学","财政学","国际经济与贸易","金融学","税务","其他"],"商学院":["财务管理","电子商务","工商管理","人力资源管理","市场营销","会计学","旅游管理","物流管理","其他"],"外语学院":["英语","俄语","日语","法语","德语","西班牙语","其他"],"法学院":["法学","其他"],"管理学院":["信息管理与信息系统","行政管理","劳动与社会保障","档案学","图书馆学","其他"],"社会与政治学院":["社会学","社会工作","政治学与行政学","其他"],"艺术学院":["艺术设计","绘画","音乐表演","导演","其他"],"国际商学院":["会计","金融管理与实务","其他"],"其他":["其他"]};
	var school = document.getElementById(schoolstr);
    for(var data in datas)
	{
		var option = document.createElement("option");
		option.value = data;
		option.innerHTML = data;
		school.appendChild(option);
	}
    school.onchange = function()
	{
		var selectItem  = this.value;
		var departs = document.getElementById(departmentstr);
		for(var index = departs.options.length-1;index>=0;index--)
		{
			var depart = departs[index];
			departs.removeChild(depart);
		}
		if(selectItem.value == "null")
		{
			return ;
		}
		var selectSchool = datas[selectItem];
		for(var i=0;i<selectSchool.length;i++)
		{
			var option2 = document.createElement("option");
			option2.value = selectSchool[i];
			option2.innerHTML = selectSchool[i];
			departs.appendChild(option2);
		} 
	};
}
function checkAccount()
{
	if (document.getElementById("loginusername").value=="")
	{
		alert("用户名不能为空！");
		return false;
	}
	else if(document.getElementById("loginuserpsw").value=="")
	{
		alert("密码不能为空！");
		return false;
	}
	return true;
}
function checkRegisterInfo()
{
	if(document.getElementById("reguserno").value=="")
	{
		alert("学号不能为空！");
		return false;
	}
	else if(document.getElementById("regusername").value=="")
	{
		alert("昵称不能为空！");
		return false;
	}
	else if(document.getElementById("reguserpsw").value=="")
	{
		alert("密码不能为空！");
		return false;
	}
	else if(document.getElementById("reguseremail").value=="")
	{
		alert("邮箱不能为空！");
		return false;
	}
	else if(document.getElementById("reguserschool").selectedIndex==0)
	{
		alert("请选择学院！");
		return false;
	}
	else if(!document.getElementById("regagree").checked)
	{
		alert("亲，不同意协议是不能注册的！");
		return false;
	}
	var namepattern = /^[a-zA-Z0-9_]{6,20}/;
	if(!namepattern.test(document.getElementById("regusername").value))
    	{
        alert("昵称中只能为英文数字和下划线且长度在6~20之间！");
        return false;
   	}
	var pswpattern = /^[a-zA-Z0-9_-]{6,20}/;
	if(!pswpattern.test(document.getElementById("reguserpsw").value))
    	{
        alert("密码中含有非法字符或者长度不在6~20之间！");
        return false;
   	}
  	var nopattern = /^[a-zA-Z]{1}(\d){8,9}/;
	if(!nopattern.test(document.getElementById("reguserno").value))
    	{
        alert("请检查学号是否正确！");
        return false;
   	}
	var pattern = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
	if(!pattern.test(document.getElementById("reguseremail").value))
	{
		alert("非法的电子邮件");
		return false;
	 }
	return true;
}
function checkUpload()
{
	var paperfilename=document.getElementById("paperfile").value;
	if(document.getElementById("papercourse").value=="")
	{
		alert("课程名不能为空！");
		return false;
	}
	else if(paperfilename=="")
	{
		alert("请上传附件！");
		return false;
	}
	else if(paperfilename.substr(paperfilename.length-4,4)!=".doc"&&paperfilename.substr(paperfilename.length-4,4)!=".pdf"&&paperfilename.substr(paperfilename.length-5,5)!=".docx"&&paperfilename.substr(paperfilename.length-4,4)!=".DOC"&&paperfilename.substr(paperfilename.length-4,4)!=".PDF"&&paperfilename.substr(paperfilename.length-5,5)!=".DOCX"&&paperfilename.substr(paperfilename.length-4,4)!=".wps"&&paperfilename.substr(paperfilename.length-4,4)!=".WPS")
	{
		alert("附件上传格式只能是.doc|.docx|.wps或.pdf");
		return false;
	}
	return true;
}
function changevisibility()
{
	if (checkUpload())
	{
		document.getElementById("uploadstate").style.display="inline";
	}
}
//****
function fcheckUpload()
{
	var paperfilename=document.getElementById("fpaperfile").value;
	if(document.getElementById("fpapercourse").value=="")
	{
		alert("课程名不能为空！");
		return false;
	}
	else if(paperfilename=="")
	{
		alert("请上传附件！");
		return false;
	}
	else if(paperfilename.substr(paperfilename.length-4,4)!=".doc"&&paperfilename.substr(paperfilename.length-4,4)!=".pdf"&&paperfilename.substr(paperfilename.length-5,5)!=".docx"&&paperfilename.substr(paperfilename.length-4,4)!=".DOC"&&paperfilename.substr(paperfilename.length-4,4)!=".PDF"&&paperfilename.substr(paperfilename.length-5,5)!=".DOCX"&&paperfilename.substr(paperfilename.length-4,4)!=".wps"&&paperfilename.substr(paperfilename.length-4,4)!=".WPS")
	{
		alert("附件上传格式只能是.doc|.docx|.wps或.pdf");
		return false;
	}
	return true;
}
function fchangevisibility()
{
	if (fcheckUpload())
	{
		document.getElementById("fuploadstate").style.display="inline";
	}
}
//****
function checkComment()
{
	if(document.getElementById("commentnickname").value=="")
	{
		alert("昵称不能为空！");
		return false;
	}
	if(document.getElementById("commentemail").value!="")
	{
		var pattern = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
		if(!pattern.test(document.getElementById("commentemail").value))
		{
			alert("非法的电子邮件");
			return false;
		 }
	}
	if(document.getElementById("commentcontent").value=="")
	{
		alert("评论内容不能为空！");
		return false;
	}
	if(document.getElementById("commentcontent").value.length>500)
	{
		alert("输入的评论有点长哦！缩减到500字以内吧！");
		return false;
	}
	return true;
}