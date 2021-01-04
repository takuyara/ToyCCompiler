; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define i32 @"main"() 
{
main.block:
  %"a" = alloca i32
  %"b" = alloca i32
  %"c" = alloca i32
  %".2" = getelementptr inbounds [5 x i8], [5 x i8]* @".str_id_1", i32 0, i32 0
  %".3" = call i32 (i8*, ...) @"scanf"(i8* %".2", i32* %"a", i32* %"b")
  %".4" = load i32, i32* %"a"
  %".5" = load i32, i32* %"b"
  %".6" = add i32 %".4", %".5"
  store i32 %".6", i32* %"c"
  %".8" = load i32, i32* %"c"
  %".9" = getelementptr inbounds [4 x i8], [4 x i8]* @".str_id_2", i32 0, i32 0
  %".10" = load i32, i32* %"c"
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".9", i32 %".10")
  ret i32 0
}

declare i32 @"scanf"(i8* %".1", ...) 

@".str_id_1" = constant [5 x i8] c"%d%d\00"
declare i32 @"printf"(i8* %".1", ...) 

@".str_id_2" = constant [4 x i8] c"%d\0a\00"