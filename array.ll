; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

@"a" = internal global [10000 x i32] undef
@"n" = internal global i32 undef
@"i" = internal global i32 undef
@"sum" = internal global i32 undef
define i32 @"main"() 
{
main.block:
  %".2" = getelementptr inbounds [3 x i8], [3 x i8]* @".str_id_1", i32 0, i32 0
  %".3" = call i32 (i8*, ...) @"scanf"(i8* %".2", i32* @"n")
  store i32 1, i32* @"i"
  br label %".5"
.5:
  %".9" = load i32, i32* @"i"
  %".10" = load i32, i32* @"n"
  %".11" = icmp sle i32 %".9", %".10"
  br i1 %".11", label %".6", label %".7"
.6:
  %".13" = getelementptr inbounds [3 x i8], [3 x i8]* @".str_id_2", i32 0, i32 0
  %".14" = load i32, i32* @"i"
  %".15" = getelementptr inbounds [10000 x i32], [10000 x i32]* @"a", i32 0, i32 %".14"
  %".16" = call i32 (i8*, ...) @"scanf"(i8* %".13", i32* %".15")
  %".17" = load i32, i32* @"i"
  %".18" = add i32 %".17", 1
  store i32 %".18", i32* @"i"
  br label %".5"
.7:
  store i32 1, i32* @"i"
  br label %".22"
.22:
  %".26" = load i32, i32* @"i"
  %".27" = load i32, i32* @"n"
  %".28" = icmp sle i32 %".26", %".27"
  br i1 %".28", label %".23", label %".24"
.23:
  %".30" = load i32, i32* @"sum"
  %".31" = load i32, i32* @"i"
  %".32" = getelementptr inbounds [10000 x i32], [10000 x i32]* @"a", i32 0, i32 %".31"
  %".33" = load i32, i32* %".32"
  %".34" = add i32 %".30", %".33"
  store i32 %".34", i32* @"sum"
  %".36" = load i32, i32* @"sum"
  %".37" = load i32, i32* @"i"
  %".38" = add i32 %".37", 1
  store i32 %".38", i32* @"i"
  br label %".22"
.24:
  %".41" = getelementptr inbounds [8 x i8], [8 x i8]* @".str_id_3", i32 0, i32 0
  %".42" = load i32, i32* @"sum"
  %".43" = call i32 (i8*, ...) @"printf"(i8* %".41", i32 %".42")
  ret i32 0
}

declare i32 @"scanf"(i8* %".1", ...) 

@".str_id_1" = constant [3 x i8] c"%d\00"
@".str_id_2" = constant [3 x i8] c"%d\00"
declare i32 @"printf"(i8* %".1", ...) 

@".str_id_3" = constant [8 x i8] c"sum=%d\0a\00"