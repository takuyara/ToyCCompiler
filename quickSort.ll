; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

@"a" = internal global [1001 x i32] undef
@"InputArray" = internal global i32 undef
define void @"QuickSort"(i32 %"left", i32 %"right") 
{
QuickSort.block:
  %".4" = alloca i32
  store i32 %"left", i32* %".4"
  %".6" = alloca i32
  store i32 %"right", i32* %".6"
  %"i" = alloca i32
  %"j" = alloca i32
  %"temp" = alloca i32
  %"t" = alloca i32
  br label %".8"
.8:
  %".13" = load i32, i32* %".4"
  %".14" = load i32, i32* %".6"
  %".15" = icmp ne i32 %".14", 0
  br i1 %".15", label %".11", label %".12"
.9:
  %".19" = load i32, i32* %".4"
  %".20" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".19"
  %".21" = load i32, i32* %".20"
  store i32 %".21", i32* %"temp"
  %".23" = load i32, i32* %"temp"
  %".24" = load i32, i32* %".4"
  store i32 %".24", i32* %"i"
  %".26" = load i32, i32* %"i"
  %".27" = load i32, i32* %".6"
  store i32 %".27", i32* %"j"
  %".29" = load i32, i32* %"j"
  br label %".30"
.11:
  ret void
.12:
  br label %".9"
.30:
  %".34" = load i32, i32* %"i"
  %".35" = load i32, i32* %"j"
  %".36" = icmp ne i32 %".35", 0
  br i1 %".36", label %".31", label %".32"
.31:
  br label %".38"
.32:
  %".101" = load i32, i32* %"i"
  %".102" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".101"
  %".103" = load i32, i32* %".102"
  %".104" = load i32, i32* %".4"
  %".105" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".104"
  store i32 %".103", i32* %".105"
  %".107" = load i32, i32* %".105"
  %".108" = load i32, i32* %"temp"
  %".109" = load i32, i32* %"i"
  %".110" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".109"
  store i32 %".108", i32* %".110"
  %".112" = load i32, i32* %".110"
  %"temp1" = alloca i32
  %".113" = load i32, i32* %"i"
  %".114" = sub i32 %".113", 1
  store i32 %".114", i32* %"temp1"
  %"temp2" = alloca i32
  %".116" = load i32, i32* %"i"
  %".117" = add i32 %".116", 1
  store i32 %".117", i32* %"temp2"
  %".119" = load i32, i32* %".4"
  %".120" = load i32, i32* %"temp1"
  call void @"QuickSort"(i32 %".119", i32 %".120")
  %".122" = load i32, i32* %"temp2"
  %".123" = load i32, i32* %".6"
  call void @"QuickSort"(i32 %".122", i32 %".123")
  ret void
.38:
  %".42" = load i32, i32* %"j"
  %".43" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".42"
  %".44" = load i32, i32* %".43"
  %".45" = load i32, i32* %"temp"
  %".46" = load i32, i32* %"i"
  %".47" = load i32, i32* %"j"
  %".48" = icmp ne i32 %".47", 0
  br i1 %".48", label %".39", label %".40"
.39:
  %".50" = load i32, i32* %"j"
  %".51" = sub i32 %".50", 1
  store i32 %".51", i32* %"j"
  %".53" = load i32, i32* %"j"
  br label %".38"
.40:
  br label %".55"
.55:
  %".59" = load i32, i32* %"i"
  %".60" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".59"
  %".61" = load i32, i32* %".60"
  %".62" = load i32, i32* %"temp"
  %".63" = load i32, i32* %"i"
  %".64" = load i32, i32* %"j"
  %".65" = icmp ne i32 %".64", 0
  br i1 %".65", label %".56", label %".57"
.56:
  %".67" = load i32, i32* %"i"
  %".68" = add i32 %".67", 1
  store i32 %".68", i32* %"i"
  %".70" = load i32, i32* %"i"
  br label %".55"
.57:
  br label %".72"
.72:
  %".77" = load i32, i32* %"i"
  %".78" = load i32, i32* %"j"
  %".79" = icmp ne i32 %".78", 0
  br i1 %".79", label %".75", label %".76"
.73:
  br label %".30"
.75:
  %".81" = load i32, i32* %"i"
  %".82" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".81"
  %".83" = load i32, i32* %".82"
  store i32 %".83", i32* %"t"
  %".85" = load i32, i32* %"t"
  %".86" = load i32, i32* %"j"
  %".87" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".86"
  %".88" = load i32, i32* %".87"
  %".89" = load i32, i32* %"i"
  %".90" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".89"
  store i32 %".88", i32* %".90"
  %".92" = load i32, i32* %".90"
  %".93" = load i32, i32* %"t"
  %".94" = load i32, i32* %"j"
  %".95" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".94"
  store i32 %".93", i32* %".95"
  %".97" = load i32, i32* %".95"
  br label %".73"
.76:
  br label %".73"
}

define i32 @"main"() 
{
main.block:
  %".2" = getelementptr inbounds [24 x i8], [24 x i8]* @".str_id_1", i32 0, i32 0
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2")
  %".4" = getelementptr inbounds [3 x i8], [3 x i8]* @".str_id_2", i32 0, i32 0
  %".5" = call i32 (i8*, ...) @"scanf"(i8* %".4", i32* @"InputArray")
  %".6" = getelementptr inbounds [27 x i8], [27 x i8]* @".str_id_3", i32 0, i32 0
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6")
  %"i" = alloca i32
  %"j" = alloca i32
  %"t" = alloca i32
  store i32 0, i32* %"i"
  br label %".9"
.9:
  %".13" = load i32, i32* %"i"
  %".14" = load i32, i32* @"InputArray"
  %".15" = icmp ne i32 %".14", 0
  br i1 %".15", label %".10", label %".11"
.10:
  %".17" = getelementptr inbounds [3 x i8], [3 x i8]* @".str_id_4", i32 0, i32 0
  %".18" = load i32, i32* %"i"
  %".19" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".18"
  %".20" = call i32 (i8*, ...) @"scanf"(i8* %".17", i32* %".19")
  %".21" = load i32, i32* %"i"
  %".22" = add i32 %".21", 1
  store i32 %".22", i32* %"i"
  br label %".9"
.11:
  %"temp" = alloca i32
  %".25" = load i32, i32* @"InputArray"
  %".26" = sub i32 %".25", 1
  store i32 %".26", i32* %"temp"
  %".28" = load i32, i32* %"temp"
  call void @"QuickSort"(i32 0, i32 %".28")
  store i32 0, i32* %"i"
  br label %".31"
.31:
  %".35" = load i32, i32* %"i"
  %".36" = load i32, i32* @"InputArray"
  %".37" = icmp ne i32 %".36", 0
  br i1 %".37", label %".32", label %".33"
.32:
  %".39" = getelementptr inbounds [4 x i8], [4 x i8]* @".str_id_5", i32 0, i32 0
  %".40" = load i32, i32* %"i"
  %".41" = getelementptr inbounds [1001 x i32], [1001 x i32]* @"a", i32 0, i32 %".40"
  %".42" = load i32, i32* %".41"
  %".43" = call i32 (i8*, ...) @"printf"(i8* %".39", i32 %".42")
  %".44" = load i32, i32* %"i"
  %".45" = add i32 %".44", 1
  store i32 %".45", i32* %"i"
  br label %".31"
.33:
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...) 

@".str_id_1" = constant [24 x i8] c"Input the array length:\00"
declare i32 @"scanf"(i8* %".1", ...) 

@".str_id_2" = constant [3 x i8] c"%d\00"
@".str_id_3" = constant [27 x i8] c"Input every array element:\00"
@".str_id_4" = constant [3 x i8] c"%d\00"
@".str_id_5" = constant [4 x i8] c"%d \00"