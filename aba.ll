; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

@"a" = internal global [1000 x i8] undef
@"len" = internal global i32 undef
define i32 @"check"() 
{
check.block:
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %".3"
.3:
  %".7" = load i32, i32* %"i"
  %".8" = load i32, i32* @"len"
  %".9" = icmp slt i32 %".7", %".8"
  br i1 %".9", label %".4", label %".5"
.4:
  br label %".11"
.5:
  ret i32 1
.11:
  %".16" = load i32, i32* %"i"
  %".17" = getelementptr inbounds [1000 x i8], [1000 x i8]* @"a", i32 0, i32 %".16"
  %".18" = load i8, i8* %".17"
  %".19" = load i32, i32* @"len"
  %".20" = load i32, i32* %"i"
  %".21" = sub i32 %".19", %".20"
  %".22" = sub i32 %".21", 1
  %".23" = getelementptr inbounds [1000 x i8], [1000 x i8]* @"a", i32 0, i32 %".22"
  %".24" = load i8, i8* %".23"
  %".25" = icmp ne i8 %".18", %".24"
  br i1 %".25", label %".14", label %".15"
.12:
  %".29" = load i32, i32* %"i"
  %".30" = add i32 %".29", 1
  store i32 %".30", i32* %"i"
  br label %".3"
.14:
  ret i32 0
.15:
  br label %".12"
}

define i32 @"main"() 
{
main.block:
  %"i" = alloca i32
  %"tmpchar" = alloca i8
  %".2" = getelementptr inbounds [15 x i8], [15 x i8]* @".str_id_1", i32 0, i32 0
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2")
  %".4" = getelementptr inbounds [4 x i8], [4 x i8]* @".str_id_2", i32 0, i32 0
  %".5" = call i32 (i8*, ...) @"scanf"(i8* %".4", i32* @"len")
  %".6" = getelementptr inbounds [15 x i8], [15 x i8]* @".str_id_3", i32 0, i32 0
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6")
  %".8" = getelementptr inbounds [3 x i8], [3 x i8]* @".str_id_4", i32 0, i32 0
  %".9" = call i32 (i8*, ...) @"scanf"(i8* %".8", i8* %"tmpchar")
  store i32 0, i32* %"i"
  br label %".11"
.11:
  %".15" = load i32, i32* %"i"
  %".16" = load i32, i32* @"len"
  %".17" = icmp slt i32 %".15", %".16"
  br i1 %".17", label %".12", label %".13"
.12:
  %".19" = getelementptr inbounds [3 x i8], [3 x i8]* @".str_id_5", i32 0, i32 0
  %".20" = load i32, i32* %"i"
  %".21" = getelementptr inbounds [1000 x i8], [1000 x i8]* @"a", i32 0, i32 %".20"
  %".22" = call i32 (i8*, ...) @"scanf"(i8* %".19", i8* %".21")
  %".23" = load i32, i32* %"i"
  %".24" = add i32 %".23", 1
  store i32 %".24", i32* %"i"
  br label %".11"
.13:
  br label %".27"
.27:
  %".32" = call i32 @"check"()
  %".33" = icmp eq i32 %".32", 0
  br i1 %".33", label %".30", label %".31"
.28:
  ret i32 0
.30:
  %".35" = getelementptr inbounds [16 x i8], [16 x i8]* @".str_id_6", i32 0, i32 0
  %".36" = call i32 (i8*, ...) @"printf"(i8* %".35")
  br label %".28"
.31:
  %".38" = getelementptr inbounds [12 x i8], [12 x i8]* @".str_id_7", i32 0, i32 0
  %".39" = call i32 (i8*, ...) @"printf"(i8* %".38")
  br label %".28"
}

declare i32 @"printf"(i8* %".1", ...) 

@".str_id_1" = constant [15 x i8] c"Input length: \00"
declare i32 @"scanf"(i8* %".1", ...) 

@".str_id_2" = constant [4 x i8] c"%d%\00"
@".str_id_3" = constant [15 x i8] c"Input string: \00"
@".str_id_4" = constant [3 x i8] c"%c\00"
@".str_id_5" = constant [3 x i8] c"%c\00"
@".str_id_6" = constant [16 x i8] c"Not palindrome\0a\00"
@".str_id_7" = constant [12 x i8] c"Palindrome\0a\00"