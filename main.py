import time  # time.sleep延时

import fire

import weiban


class CLI(object):
    def search_tenant(self, tenant_name):
        for tenant_data in weiban.get_tenant_list()['data']:
            if tenant_name in tenant_data['name']:
                print(f"{tenant_data['name']} -> {tenant_data['code']}")

    def token_mode(self, tenant_code, user_id, user_project_id, token):
        """手动输入token等信息登录，您可以在README中找到浏览器console生成执行命令的代码"""
        # 请求用户信息
        try:
            print('请求用户信息')
            stu_info_response = weiban.getStuInfo(user_id,
                                                  tenant_code)
            print('用户信息：' + stu_info_response['data']['realName'] + '\n'
                  + stu_info_response['data']['orgName']
                  + stu_info_response['data']['specialtyName']
                  )
            time.sleep(2)
        except BaseException:
            print('解析用户信息失败，将尝试继续运行，请注意运行异常')

        # 请求课程完成进度
        try:
            get_progress_response = weiban.getProgress(user_project_id,
                                                       tenant_code)
            print('课程总数：' + str(get_progress_response['data']['requiredNum']) + '\n'
                  + '完成课程：' + str(get_progress_response['data']['requiredFinishedNum']) + '\n'
                  + '结束时间' + str(get_progress_response['data']['endTime']) + '\n'
                  + '剩余天数' + str(get_progress_response['data']['lastDays'])
                  )
            time.sleep(2)
        except BaseException:
            print('解析课程进度失败，将尝试继续运行，请注意运行异常')

        # 请求课程列表
        get_list_course_response = {}
        try:
            get_list_course_response = weiban.getListCourse(user_project_id,
                                                            '3',
                                                            tenant_code,
                                                            '')
            time.sleep(2)
        except BaseException:
            print('请求课程列表失败')

        print('解析课程列表并发送完成请求')

        for i in get_list_course_response['data']:
            print('\n----章节码：' + i['categoryCode'] + '章节内容：' + i['categoryName'])
            courseList = weiban.getCourseListByCategoryCode(i['categoryCode'], user_project_id, user_id, tenant_code)
            for j in courseList['data']:
                print('课程内容：' + j['resourceName'] + '\nuserCourseId:' + j['userCourseId'])

                if (j['finished'] == 1):
                    print('已完成')
                else:
                    print('发送完成请求')
                    weiban.do_study(user_project_id, j['resourceId'], tenant_code, user_id, token=token)
                    time.sleep(10)
                    weiban.finish_course(j['userCourseId'], tenant_code)

                    delayInt = weiban.getRandomTime()
                    print('\n随机延时' + str(delayInt))
                    time.sleep(delayInt)
        print('所有课程完成，若有漏刷，请再次运行')


if __name__ == '__main__':
    fire.Fire(CLI)
