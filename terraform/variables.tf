variable "region" {
    default = "ap-northeast-1"  # 適切なリージョンを設定
}

variable "ecr_repository" {
    default = "summpost"
}

variable "image_tag" {
    default = "latest"
}
