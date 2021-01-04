; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define i32 @"main"() 
{
main.block:
  %"expression" = alloca [2048 x i8]
  %"operation" = alloca [2048 x i8]
  %"numStack" = alloca [2048 x i32]
  %"nowNum" = alloca i32
  %".2" = sub i32 0, 1
  store i32 %".2", i32* %"nowNum"
  %"nowOp" = alloca i32
  %".4" = sub i32 0, 1
  store i32 %".4", i32* %"nowOp"
  %"decimal" = alloca i32
  store i32 1, i32* %"decimal"
  %"length" = alloca i32
  %"num" = alloca i32
  store i32 0, i32* %"num"
  %"i" = alloca i32
  %".8" = getelementptr inbounds [26 x i8], [26 x i8]* @".str_id_1", i32 0, i32 0
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8")
  %".10" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 0
  %".11" = call i32 (...) @"gets"(i8* %".10")
  %".12" = getelementptr inbounds [10 x i8], [10 x i8]* @".str_id_2", i32 0, i32 0
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12")
  %".14" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 0
  %".15" = call i32 @"strlen"(i8* %".14")
  store i32 %".15", i32* %"length"
  %".17" = load i32, i32* %"length"
  %".18" = load i32, i32* %"length"
  %".19" = sub i32 %".18", 1
  store i32 %".19", i32* %"i"
  br label %".21"
.21:
  %".25" = load i32, i32* %"i"
  %".26" = icmp sge i32 %".25", 0
  br i1 %".26", label %".22", label %".23"
.22:
  %".28" = load i32, i32* %"i"
  %".29" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".28"
  %".30" = load i8, i8* %".29"
  %".31" = load i32, i32* %"i"
  %".32" = add i32 %".31", 1
  %".33" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".32"
  store i8 %".30", i8* %".33"
  %".35" = load i8, i8* %".33"
  %".36" = load i32, i32* %"i"
  %".37" = sub i32 %".36", 1
  store i32 %".37", i32* %"i"
  br label %".21"
.23:
  %".40" = getelementptr inbounds [16 x i8], [16 x i8]* @".str_id_3", i32 0, i32 0
  %".41" = call i32 (i8*, ...) @"printf"(i8* %".40")
  %".42" = load i32, i32* %"length"
  %".43" = add i32 %".42", 1
  store i32 %".43", i32* %"i"
  %".45" = load i32, i32* %"i"
  %".46" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 0
  store i8 40, i8* %".46"
  %".48" = load i8, i8* %".46"
  %".49" = load i32, i32* %"length"
  %".50" = add i32 %".49", 1
  %".51" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".50"
  store i8 41, i8* %".51"
  %".53" = load i8, i8* %".51"
  %".54" = load i32, i32* %"length"
  %".55" = add i32 %".54", 2
  store i32 %".55", i32* %"length"
  %".57" = load i32, i32* %"length"
  br label %".58"
.58:
  %".62" = load i32, i32* %"i"
  %".63" = icmp sge i32 %".62", 0
  br i1 %".63", label %".59", label %".60"
.59:
  br label %".65"
.60:
  %".468" = getelementptr inbounds [11 x i8], [11 x i8]* @".str_id_4", i32 0, i32 0
  %".469" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 0
  %".470" = load i32, i32* %".469"
  %".471" = call i32 (i8*, ...) @"printf"(i8* %".468", i32 %".470")
  ret i32 0
.65:
  %".70" = load i32, i32* %"i"
  %".71" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".70"
  %".72" = load i8, i8* %".71"
  %".73" = icmp eq i8 %".72", 43
  br i1 %".73", label %".68", label %".69"
.66:
  br label %".58"
.68:
  br label %".75"
.69:
  %".154" = load i32, i32* %"i"
  %".155" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".154"
  %".156" = load i8, i8* %".155"
  %".157" = icmp eq i8 %".156", 45
  br i1 %".157", label %".152", label %".153"
.75:
  %".79" = load i32, i32* %"nowOp"
  %".80" = load i32, i32* %"nowOp"
  %".81" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".80"
  %".82" = load i8, i8* %".81"
  %".83" = icmp eq i8 %".82", 42
  %".84" = load i32, i32* %"nowOp"
  %".85" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".84"
  %".86" = load i8, i8* %".85"
  %".87" = icmp eq i8 %".86", 47
  %".88" = or i1 %".83", %".87"
  %".89" = zext i1 %".88" to i32
  %".90" = icmp sge i32 %".79", %".89"
  br i1 %".90", label %".76", label %".77"
.76:
  br label %".92"
.77:
  %".139" = load i32, i32* %"nowOp"
  %".140" = add i32 %".139", 1
  store i32 %".140", i32* %"nowOp"
  %".142" = load i32, i32* %"nowOp"
  %".143" = load i32, i32* %"nowOp"
  %".144" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".143"
  store i8 43, i8* %".144"
  %".146" = load i8, i8* %".144"
  %".147" = load i32, i32* %"i"
  %".148" = sub i32 %".147", 1
  store i32 %".148", i32* %"i"
  %".150" = load i32, i32* %"i"
  br label %".66"
.92:
  %".97" = load i32, i32* %"nowOp"
  %".98" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".97"
  %".99" = load i8, i8* %".98"
  %".100" = icmp eq i8 %".99", 42
  br i1 %".100", label %".95", label %".96"
.93:
  %".130" = load i32, i32* %"nowOp"
  %".131" = sub i32 %".130", 1
  store i32 %".131", i32* %"nowOp"
  %".133" = load i32, i32* %"nowOp"
  %".134" = load i32, i32* %"nowNum"
  %".135" = sub i32 %".134", 1
  store i32 %".135", i32* %"nowNum"
  %".137" = load i32, i32* %"nowNum"
  br label %".75"
.95:
  %".102" = load i32, i32* %"nowNum"
  %".103" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".102"
  %".104" = load i32, i32* %".103"
  %".105" = load i32, i32* %"nowNum"
  %".106" = sub i32 %".105", 1
  %".107" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".106"
  %".108" = load i32, i32* %".107"
  %".109" = mul i32 %".104", %".108"
  %".110" = load i32, i32* %"nowNum"
  %".111" = sub i32 %".110", 1
  %".112" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".111"
  store i32 %".109", i32* %".112"
  %".114" = load i32, i32* %".112"
  br label %".93"
.96:
  %".116" = load i32, i32* %"nowNum"
  %".117" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".116"
  %".118" = load i32, i32* %".117"
  %".119" = load i32, i32* %"nowNum"
  %".120" = sub i32 %".119", 1
  %".121" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".120"
  %".122" = load i32, i32* %".121"
  %".123" = sdiv i32 %".118", %".122"
  %".124" = load i32, i32* %"nowNum"
  %".125" = sub i32 %".124", 1
  %".126" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".125"
  store i32 %".123", i32* %".126"
  %".128" = load i32, i32* %".126"
  br label %".93"
.152:
  br label %".159"
.153:
  %".238" = load i32, i32* %"i"
  %".239" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".238"
  %".240" = load i8, i8* %".239"
  %".241" = icmp eq i8 %".240", 42
  br i1 %".241", label %".236", label %".237"
.159:
  %".163" = load i32, i32* %"nowOp"
  %".164" = load i32, i32* %"nowOp"
  %".165" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".164"
  %".166" = load i8, i8* %".165"
  %".167" = icmp eq i8 %".166", 42
  %".168" = load i32, i32* %"nowOp"
  %".169" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".168"
  %".170" = load i8, i8* %".169"
  %".171" = icmp eq i8 %".170", 47
  %".172" = or i1 %".167", %".171"
  %".173" = zext i1 %".172" to i32
  %".174" = icmp sge i32 %".163", %".173"
  br i1 %".174", label %".160", label %".161"
.160:
  br label %".176"
.161:
  %".223" = load i32, i32* %"nowOp"
  %".224" = add i32 %".223", 1
  store i32 %".224", i32* %"nowOp"
  %".226" = load i32, i32* %"nowOp"
  %".227" = load i32, i32* %"nowOp"
  %".228" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".227"
  store i8 45, i8* %".228"
  %".230" = load i8, i8* %".228"
  %".231" = load i32, i32* %"i"
  %".232" = sub i32 %".231", 1
  store i32 %".232", i32* %"i"
  %".234" = load i32, i32* %"i"
  br label %".66"
.176:
  %".181" = load i32, i32* %"nowOp"
  %".182" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".181"
  %".183" = load i8, i8* %".182"
  %".184" = icmp eq i8 %".183", 42
  br i1 %".184", label %".179", label %".180"
.177:
  %".214" = load i32, i32* %"nowNum"
  %".215" = sub i32 %".214", 1
  store i32 %".215", i32* %"nowNum"
  %".217" = load i32, i32* %"nowNum"
  %".218" = load i32, i32* %"nowOp"
  %".219" = sub i32 %".218", 1
  store i32 %".219", i32* %"nowOp"
  %".221" = load i32, i32* %"nowOp"
  br label %".159"
.179:
  %".186" = load i32, i32* %"nowNum"
  %".187" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".186"
  %".188" = load i32, i32* %".187"
  %".189" = load i32, i32* %"nowNum"
  %".190" = sub i32 %".189", 1
  %".191" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".190"
  %".192" = load i32, i32* %".191"
  %".193" = mul i32 %".188", %".192"
  %".194" = load i32, i32* %"nowNum"
  %".195" = sub i32 %".194", 1
  %".196" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".195"
  store i32 %".193", i32* %".196"
  %".198" = load i32, i32* %".196"
  br label %".177"
.180:
  %".200" = load i32, i32* %"nowNum"
  %".201" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".200"
  %".202" = load i32, i32* %".201"
  %".203" = load i32, i32* %"nowNum"
  %".204" = sub i32 %".203", 1
  %".205" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".204"
  %".206" = load i32, i32* %".205"
  %".207" = sdiv i32 %".202", %".206"
  %".208" = load i32, i32* %"nowNum"
  %".209" = sub i32 %".208", 1
  %".210" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".209"
  store i32 %".207", i32* %".210"
  %".212" = load i32, i32* %".210"
  br label %".177"
.236:
  %".243" = load i32, i32* %"nowOp"
  %".244" = add i32 %".243", 1
  store i32 %".244", i32* %"nowOp"
  %".246" = load i32, i32* %"nowOp"
  %".247" = load i32, i32* %"nowOp"
  %".248" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".247"
  store i8 42, i8* %".248"
  %".250" = load i8, i8* %".248"
  %".251" = load i32, i32* %"i"
  %".252" = sub i32 %".251", 1
  store i32 %".252", i32* %"i"
  %".254" = load i32, i32* %"i"
  br label %".66"
.237:
  %".258" = load i32, i32* %"i"
  %".259" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".258"
  %".260" = load i8, i8* %".259"
  %".261" = icmp eq i8 %".260", 47
  br i1 %".261", label %".256", label %".257"
.256:
  %".263" = load i32, i32* %"nowOp"
  %".264" = add i32 %".263", 1
  store i32 %".264", i32* %"nowOp"
  %".266" = load i32, i32* %"nowOp"
  %".267" = load i32, i32* %"nowOp"
  %".268" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".267"
  store i8 47, i8* %".268"
  %".270" = load i8, i8* %".268"
  %".271" = load i32, i32* %"i"
  %".272" = sub i32 %".271", 1
  store i32 %".272", i32* %"i"
  %".274" = load i32, i32* %"i"
  br label %".66"
.257:
  %".278" = load i32, i32* %"i"
  %".279" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".278"
  %".280" = load i8, i8* %".279"
  %".281" = icmp eq i8 %".280", 41
  br i1 %".281", label %".276", label %".277"
.276:
  %".283" = load i32, i32* %"nowOp"
  %".284" = add i32 %".283", 1
  store i32 %".284", i32* %"nowOp"
  %".286" = load i32, i32* %"nowOp"
  %".287" = load i32, i32* %"nowOp"
  %".288" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".287"
  store i8 41, i8* %".288"
  %".290" = load i8, i8* %".288"
  %".291" = load i32, i32* %"i"
  %".292" = sub i32 %".291", 1
  store i32 %".292", i32* %"i"
  %".294" = load i32, i32* %"i"
  br label %".66"
.277:
  %".298" = load i32, i32* %"i"
  %".299" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".298"
  %".300" = load i8, i8* %".299"
  %".301" = icmp eq i8 %".300", 40
  br i1 %".301", label %".296", label %".297"
.296:
  br label %".303"
.297:
  store i32 0, i32* %"num"
  %".415" = load i32, i32* %"num"
  store i32 1, i32* %"decimal"
  %".417" = load i32, i32* %"decimal"
  br label %".418"
.303:
  %".307" = load i32, i32* %"nowOp"
  %".308" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".307"
  %".309" = load i8, i8* %".308"
  %".310" = icmp ne i8 %".309", 41
  br i1 %".310", label %".304", label %".305"
.304:
  %"OperatorGet" = alloca i8
  %".312" = load i32, i32* %"nowOp"
  %".313" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"operation", i32 0, i32 %".312"
  %".314" = load i8, i8* %".313"
  store i8 %".314", i8* %"OperatorGet"
  %".316" = load i32, i32* %"nowOp"
  %".317" = sub i32 %".316", 1
  store i32 %".317", i32* %"nowOp"
  %".319" = load i32, i32* %"nowOp"
  br label %".320"
.305:
  %".405" = load i32, i32* %"nowOp"
  %".406" = sub i32 %".405", 1
  store i32 %".406", i32* %"nowOp"
  %".408" = load i32, i32* %"nowOp"
  %".409" = load i32, i32* %"i"
  %".410" = sub i32 %".409", 1
  store i32 %".410", i32* %"i"
  %".412" = load i32, i32* %"i"
  br label %".66"
.320:
  %".325" = load i8, i8* %"OperatorGet"
  %".326" = icmp eq i8 %".325", 43
  br i1 %".326", label %".323", label %".324"
.321:
  %".400" = load i32, i32* %"nowNum"
  %".401" = sub i32 %".400", 1
  store i32 %".401", i32* %"nowNum"
  %".403" = load i32, i32* %"nowNum"
  br label %".303"
.323:
  %".328" = load i32, i32* %"nowNum"
  %".329" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".328"
  %".330" = load i32, i32* %".329"
  %".331" = load i32, i32* %"nowNum"
  %".332" = sub i32 %".331", 1
  %".333" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".332"
  %".334" = load i32, i32* %".333"
  %".335" = add i32 %".330", %".334"
  %".336" = load i32, i32* %"nowNum"
  %".337" = sub i32 %".336", 1
  %".338" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".337"
  store i32 %".335", i32* %".338"
  %".340" = load i32, i32* %".338"
  br label %".321"
.324:
  %".344" = load i8, i8* %"OperatorGet"
  %".345" = icmp eq i8 %".344", 45
  br i1 %".345", label %".342", label %".343"
.342:
  %".347" = load i32, i32* %"nowNum"
  %".348" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".347"
  %".349" = load i32, i32* %".348"
  %".350" = load i32, i32* %"nowNum"
  %".351" = sub i32 %".350", 1
  %".352" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".351"
  %".353" = load i32, i32* %".352"
  %".354" = sub i32 %".349", %".353"
  %".355" = load i32, i32* %"nowNum"
  %".356" = sub i32 %".355", 1
  %".357" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".356"
  store i32 %".354", i32* %".357"
  %".359" = load i32, i32* %".357"
  br label %".321"
.343:
  %".363" = load i8, i8* %"OperatorGet"
  %".364" = icmp eq i8 %".363", 47
  br i1 %".364", label %".361", label %".362"
.361:
  %".366" = load i32, i32* %"nowNum"
  %".367" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".366"
  %".368" = load i32, i32* %".367"
  %".369" = load i32, i32* %"nowNum"
  %".370" = sub i32 %".369", 1
  %".371" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".370"
  %".372" = load i32, i32* %".371"
  %".373" = sdiv i32 %".368", %".372"
  %".374" = load i32, i32* %"nowNum"
  %".375" = sub i32 %".374", 1
  %".376" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".375"
  store i32 %".373", i32* %".376"
  %".378" = load i32, i32* %".376"
  br label %".321"
.362:
  %".382" = load i8, i8* %"OperatorGet"
  %".383" = icmp eq i8 %".382", 42
  br i1 %".383", label %".380", label %".381"
.380:
  %".385" = load i32, i32* %"nowNum"
  %".386" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".385"
  %".387" = load i32, i32* %".386"
  %".388" = load i32, i32* %"nowNum"
  %".389" = sub i32 %".388", 1
  %".390" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".389"
  %".391" = load i32, i32* %".390"
  %".392" = mul i32 %".387", %".391"
  %".393" = load i32, i32* %"nowNum"
  %".394" = sub i32 %".393", 1
  %".395" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".394"
  store i32 %".392", i32* %".395"
  %".397" = load i32, i32* %".395"
  br label %".321"
.381:
  br label %".321"
.418:
  %".422" = load i32, i32* %"i"
  %".423" = load i32, i32* %"i"
  %".424" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".423"
  %".425" = load i8, i8* %".424"
  %".426" = sext i8 %".425" to i32
  %".427" = icmp sge i32 %".422", %".426"
  %".428" = load i32, i32* %"i"
  %".429" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".428"
  %".430" = load i8, i8* %".429"
  %".431" = zext i1 %".427" to i8
  %".432" = icmp sle i8 %".431", %".430"
  %".433" = zext i1 %".432" to i8
  %".434" = icmp sge i8 %".433", 48
  br i1 %".434", label %".419", label %".420"
.419:
  %".436" = load i32, i32* %"num"
  %".437" = load i32, i32* %"i"
  %".438" = getelementptr inbounds [2048 x i8], [2048 x i8]* %"expression", i32 0, i32 %".437"
  %".439" = load i8, i8* %".438"
  %".440" = sub i8 %".439", 48
  %".441" = sext i8 %".440" to i32
  %".442" = add i32 %".436", %".441"
  %".443" = load i32, i32* %"decimal"
  %".444" = mul i32 %".442", %".443"
  store i32 %".444", i32* %"num"
  %".446" = load i32, i32* %"num"
  %".447" = load i32, i32* %"decimal"
  %".448" = mul i32 %".447", 10
  store i32 %".448", i32* %"decimal"
  %".450" = load i32, i32* %"decimal"
  %".451" = load i32, i32* %"i"
  %".452" = sub i32 %".451", 1
  store i32 %".452", i32* %"i"
  %".454" = load i32, i32* %"i"
  br label %".418"
.420:
  %".456" = load i32, i32* %"num"
  %".457" = load i32, i32* %"nowNum"
  %".458" = add i32 %".457", 1
  %".459" = getelementptr inbounds [2048 x i32], [2048 x i32]* %"numStack", i32 0, i32 %".458"
  store i32 %".456", i32* %".459"
  %".461" = load i32, i32* %".459"
  %".462" = load i32, i32* %"nowNum"
  %".463" = add i32 %".462", 1
  store i32 %".463", i32* %"nowNum"
  %".465" = load i32, i32* %"nowNum"
  br label %".66"
}

declare i32 @"printf"(i8* %".1", ...) 

@".str_id_1" = constant [26 x i8] c"Please input expression: \00"
declare i32 @"gets"(...) 

@".str_id_2" = constant [10 x i8] c"Gets done\00"
declare i32 @"strlen"(i8* %".1") 

@".str_id_3" = constant [16 x i8] c"Expression done\00"
@".str_id_4" = constant [11 x i8] c"Result=%d\0a\00"