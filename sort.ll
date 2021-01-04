; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

@"a" = internal global [1000 x i32] undef
@"n" = internal global i32 undef
@"i" = internal global i32 undef
define void @"sort"(i32 %"l", i32 %"r") 
{
sort.block:
  %".4" = alloca i32
  store i32 %"l", i32* %".4"
  %".6" = alloca i32
  store i32 %"r", i32* %".6"
  %"i" = alloca i32
  %".8" = load i32, i32* %".4"
  store i32 %".8", i32* %"i"
  %"j" = alloca i32
  %".10" = load i32, i32* %".6"
  store i32 %".10", i32* %"j"
  %"x" = alloca i32
  %".12" = load i32, i32* %".4"
  %".13" = getelementptr inbounds [1000 x i32], [1000 x i32]* @"a", i32 0, i32 %".12"
  %".14" = load i32, i32* %".13"
  store i32 %".14", i32* %"x"
  %"t" = alloca i32
  br label %".16"
.16:
  %".20" = load i32, i32* %"i"
  %".21" = load i32, i32* %"j"
  %".22" = icmp sle i32 %".20", %".21"
  br i1 %".22", label %".17", label %".18"
.17:
  br label %".24"
.18:
  br label %".91"
.24:
  %".28" = load i32, i32* %"i"
  %".29" = getelementptr inbounds [1000 x i32], [1000 x i32]* @"a", i32 0, i32 %".28"
  %".30" = load i32, i32* %".29"
  %".31" = load i32, i32* %"x"
  %".32" = icmp slt i32 %".30", %".31"
  br i1 %".32", label %".25", label %".26"
.25:
  %".34" = load i32, i32* %"i"
  %".35" = add i32 %".34", 1
  store i32 %".35", i32* %"i"
  %".37" = load i32, i32* %"i"
  br label %".24"
.26:
  br label %".39"
.39:
  %".43" = load i32, i32* %"j"
  %".44" = getelementptr inbounds [1000 x i32], [1000 x i32]* @"a", i32 0, i32 %".43"
  %".45" = load i32, i32* %".44"
  %".46" = load i32, i32* %"x"
  %".47" = icmp sgt i32 %".45", %".46"
  br i1 %".47", label %".40", label %".41"
.40:
  %".49" = load i32, i32* %"j"
  %".50" = sub i32 %".49", 1
  store i32 %".50", i32* %"j"
  %".52" = load i32, i32* %"j"
  br label %".39"
.41:
  br label %".54"
.54:
  %".59" = load i32, i32* %"i"
  %".60" = load i32, i32* %"j"
  %".61" = icmp sle i32 %".59", %".60"
  br i1 %".61", label %".57", label %".58"
.55:
  br label %".16"
.57:
  %".63" = load i32, i32* %"i"
  %".64" = getelementptr inbounds [1000 x i32], [1000 x i32]* @"a", i32 0, i32 %".63"
  %".65" = load i32, i32* %".64"
  store i32 %".65", i32* %"t"
  %".67" = load i32, i32* %"t"
  %".68" = load i32, i32* %"j"
  %".69" = getelementptr inbounds [1000 x i32], [1000 x i32]* @"a", i32 0, i32 %".68"
  %".70" = load i32, i32* %".69"
  %".71" = load i32, i32* %"i"
  %".72" = getelementptr inbounds [1000 x i32], [1000 x i32]* @"a", i32 0, i32 %".71"
  store i32 %".70", i32* %".72"
  %".74" = load i32, i32* %".72"
  %".75" = load i32, i32* %"t"
  %".76" = load i32, i32* %"j"
  %".77" = getelementptr inbounds [1000 x i32], [1000 x i32]* @"a", i32 0, i32 %".76"
  store i32 %".75", i32* %".77"
  %".79" = load i32, i32* %".77"
  %".80" = load i32, i32* %"i"
  %".81" = add i32 %".80", 1
  store i32 %".81", i32* %"i"
  %".83" = load i32, i32* %"i"
  %".84" = load i32, i32* %"j"
  %".85" = sub i32 %".84", 1
  store i32 %".85", i32* %"j"
  %".87" = load i32, i32* %"j"
  br label %".55"
.58:
  br label %".55"
.91:
  %".96" = load i32, i32* %".4"
  %".97" = load i32, i32* %"j"
  %".98" = icmp slt i32 %".96", %".97"
  br i1 %".98", label %".94", label %".95"
.92:
  br label %".105"
.94:
  %".100" = load i32, i32* %".4"
  %".101" = load i32, i32* %"j"
  call void @"sort"(i32 %".100", i32 %".101")
  br label %".92"
.95:
  br label %".92"
.105:
  %".110" = load i32, i32* %"i"
  %".111" = load i32, i32* %".6"
  %".112" = icmp slt i32 %".110", %".111"
  br i1 %".112", label %".108", label %".109"
.106:
  ret void
.108:
  %".114" = load i32, i32* %"i"
  %".115" = load i32, i32* %".6"
  call void @"sort"(i32 %".114", i32 %".115")
  br label %".106"
.109:
  br label %".106"
}

define i32 @"main"() 
{
main.block:
  %".2" = getelementptr inbounds [15 x i8], [15 x i8]* @".str_id_1", i32 0, i32 0
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2")
  %".4" = getelementptr inbounds [3 x i8], [3 x i8]* @".str_id_2", i32 0, i32 0
  %".5" = call i32 (i8*, ...) @"scanf"(i8* %".4", i32* @"n")
  %".6" = getelementptr inbounds [14 x i8], [14 x i8]* @".str_id_3", i32 0, i32 0
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6")
  store i32 1, i32* @"i"
  br label %".9"
.9:
  %".13" = load i32, i32* @"i"
  %".14" = load i32, i32* @"n"
  %".15" = icmp sle i32 %".13", %".14"
  br i1 %".15", label %".10", label %".11"
.10:
  %".17" = getelementptr inbounds [3 x i8], [3 x i8]* @".str_id_4", i32 0, i32 0
  %".18" = load i32, i32* @"i"
  %".19" = getelementptr inbounds [1000 x i32], [1000 x i32]* @"a", i32 0, i32 %".18"
  %".20" = call i32 (i8*, ...) @"scanf"(i8* %".17", i32* %".19")
  %".21" = load i32, i32* @"i"
  %".22" = add i32 %".21", 1
  store i32 %".22", i32* @"i"
  br label %".9"
.11:
  %".25" = load i32, i32* @"n"
  call void @"sort"(i32 1, i32 %".25")
  store i32 1, i32* @"i"
  br label %".28"
.28:
  %".32" = load i32, i32* @"i"
  %".33" = load i32, i32* @"n"
  %".34" = icmp sle i32 %".32", %".33"
  br i1 %".34", label %".29", label %".30"
.29:
  %".36" = getelementptr inbounds [4 x i8], [4 x i8]* @".str_id_5", i32 0, i32 0
  %".37" = load i32, i32* @"i"
  %".38" = getelementptr inbounds [1000 x i32], [1000 x i32]* @"a", i32 0, i32 %".37"
  %".39" = load i32, i32* %".38"
  %".40" = call i32 (i8*, ...) @"printf"(i8* %".36", i32 %".39")
  %".41" = load i32, i32* @"i"
  %".42" = add i32 %".41", 1
  store i32 %".42", i32* @"i"
  br label %".28"
.30:
  %".45" = getelementptr inbounds [2 x i8], [2 x i8]* @".str_id_6", i32 0, i32 0
  %".46" = call i32 (i8*, ...) @"printf"(i8* %".45")
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...) 

@".str_id_1" = constant [15 x i8] c"Input length: \00"
declare i32 @"scanf"(i8* %".1", ...) 

@".str_id_2" = constant [3 x i8] c"%d\00"
@".str_id_3" = constant [14 x i8] c"Input array: \00"
@".str_id_4" = constant [3 x i8] c"%d\00"
@".str_id_5" = constant [4 x i8] c"%d \00"
@".str_id_6" = constant [2 x i8] c"\0a\00"