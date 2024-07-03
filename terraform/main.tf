resource "aws_ecs_cluster" "main" {
    name = "summpost-cluster"
}

resource "aws_iam_role" "ecs_task_execution_role" {
    name = "ecsTaskExecutionRole"

    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
            Action = "sts:AssumeRole",
            Effect = "Allow",
            Principal = {
                Service = "ecs-tasks.amazonaws.com"
            }
            }
        ]
    })

    managed_policy_arns = [
        "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
    ]
}

resource "aws_ecs_task_definition" "main" {
    family                   = "summpost-task"
    network_mode             = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
    container_definitions    = file("ecs_task_definition.json")
    cpu                      = "256"
    memory                   = "512"
}

resource "aws_ecs_service" "main" {
    name            = "summpost-service"
    cluster         = aws_ecs_cluster.main.id
    task_definition = aws_ecs_task_definition.main.arn
    desired_count   = 1

    network_configuration {
        subnets          = [/* Your Subnets */]
        security_groups  = [/* Your Security Groups */]
        assign_public_ip = true
    }
}

resource "aws_cloudwatch_log_group" "main" {
    name              = "/ecs/summpost"
    retention_in_days = 7
}
