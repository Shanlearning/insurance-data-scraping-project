#################################################
# 重新定位方程
re_str_collapse<-function(pattern,text){
  
  position_end <- text %>% nchar() %>% cumsum()
  position_begin <- c(0,position_end) %>% .[1:(length(.)-1)] +1 
  word <- paste0(text,collapse="")
  
  word_poc <- cbind(position_begin,position_end) %>% data.table()
  
  result <- re_str_locate_all(pattern,word)
  result$start<-as.numeric(result$start)
  result$end<-as.numeric(result$end)
  
  output<-list()
  for(i in 1:dim(result)[1]){
    output[[i]] <- which( (position_begin <= result$start[i])&(position_end >= result$start[i]) ):
      which( (position_begin <= result$end[i])&(position_end >= result$end[i]) )
  }
  
  return(output)
}
#############################################################
# 给空字符向量赋值
re_str_assign_empty<-function(pattern,text,object="vector"){
  pattern<-shan_check_pattern(pattern)
  shan_f <- function(x){x[x==""]<-pattern;return(x)}
  if(object == "vector"){
    if(!is.vector(text)){warning("text is not a vector")}
    text[text==""] <- pattern;return(text)
  }else if(object == "list"){
    if(!is.list(text)){warning("text is not a list")}
    return(sapply(text,shan_f))
  }else if(object == "df"){
    if(!(is.data.frame(text)|is.data.table(text))){warning("text is not datatable or dataframe")}
    return(apply(text,2,shan_f))
  }
}
###############################################################
re_str_extract_around<-function(pattern,dat,dist){
  m <- gregexpr(pattern, dat)
  start<-m[[1]]-dist
  end<-m[[1]]+attr(m[[1]],"match.length")+dist
return(str_sub(dat,start=start,end=end))
}
################################################################